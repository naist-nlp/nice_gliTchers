from gec_metrics.metrics import MetricBaseForReferenceFree
from dataclasses import dataclass
from openai import OpenAI
from pydantic import BaseModel
import hashlib
import json
import os

class LLMSent(MetricBaseForReferenceFree):
    '''LLM-based metrics based on Kobayashi+24 https://aclanthology.org/2024.bea-1.6/.
    Note that the prompt format is modified to the shared task setting.
    '''
    @dataclass
    class Config(MetricBaseForReferenceFree.Config):
        model: str = 'gpt-4o-mini'
        organization: str = None
        project: str = None
        cache: str = None
        seed: int = 777
        verbose: bool = True
        instruction_template: str = '''The goal of this task is to rank the presented targets based on the quality of the sentences.
After reading the source, please assign a score from a minimum of 1 point to a maximum of 5 points to the target based on the quality of the sentence.

# source
[SOURCE]

# targets
[CORRECTION]

# output format
The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":
```json
{
"target_score": int // assigned score for target
}
'''

    class LLMSentOutputFormat(BaseModel):
        target_score: int
        
    def __init__(self, config: Config = None):
        super().__init__(config)
        self.client = OpenAI(
            organization=self.config.organization,
            project=self.config.project,
        )
        if self.config.cache is None:
            self.config.cache = self.config.model + '.cache'
        if os.path.exists(self.config.cache):                                                          
            self.cache = self.load_json(self.config.cache)
        else:
            self.cache = dict()
        assert '[SOURCE]' in self.config.instruction_template
        assert '[CORRECTION]' in self.config.instruction_template

    def serialize(self, obj):
        if isinstance(obj, dict):
            return {k: self.serialize(v) for k, v in obj.items()}
        elif hasattr(obj, "__dict__"):
            return self.serialize(obj.__dict__)
        elif isinstance(obj, list):
            return [self.serialize(v) for v in obj]
        else:
            return obj
        
    def create_hash(self, prompt):                                                                                     
        return hashlib.md5(prompt.encode()).hexdigest()

    def load_json(self, file_name):
        data = dict()
        with open(file_name) as f:
            json_lines = f.readlines()
            for line in json_lines:
                json_obj = json.loads(line)
                data[json_obj['id']] = json_obj['results']

        return data

    def append_to_jsonl(self, file_name, data):
        with open(file_name, 'a') as file:
            json_str = json.dumps(data, ensure_ascii=False)
            file.write(json_str + '\n')
    
    def score_sentence(
        self,
        sources: list[str],
        hypotheses: list[str]
    ) -> list[float]:
        scores = []
        for src, hyp in zip(sources, hypotheses):
            # Fill in the source and hypothesis in the template    
            instruction = self.config.instruction_template.replace(
                '[SOURCE]', src
            ).replace(
                '[CORRECTION]', hyp
            )

            _hash = self.create_hash(instruction)
            if _hash not in self.cache:
                # Call OpenAI
                if self.config.verbose:
                    print('Call API')
                response = self.client.beta.chat.completions.parse(                                                                            
                    model=self.config.model,
                    messages=[                                         
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": instruction},
                    ],
                    seed=self.config.seed,
                    response_format=self.LLMSentOutputFormat
                )
                # To avoid call OpenAI twice for the same input,
                #    we cache the results.
                response = self.serialize(response)
                save_data = {'id': _hash, 'results': response}
                self.append_to_jsonl(self.config.cache, save_data)
                self.cache[_hash] = response
            else:
                # If the same input was already processed,
                #   we simply restore the results from the cache.
                response = self.cache[_hash]
            score = json.loads(
                response['choices'][0]['message']['content']
            )['target_score']
            scores.append(score)
        return scores