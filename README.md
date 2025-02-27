# nlp2025-eval-sharedtask-gec
A tools for the shared task regarding hacking Grammatical Error Correction metrics.

# Minimal Installation
```sh
pip install git+https://github.com/naist-nlp/nice_gliTchers
python -m spacy download en_core_web_sm
```
Or
```
git clone https://github.com/naist-nlp/nice_gliTchers
cd nice_gliTchers
pip install -e ./
python -m spacy download en_core_web_sm
```

# Tutorial

### Define your Corrector

If the corrector makes correction, use `nice_glitchers.correctors.CorrectorBase`.

```python
from nice_glitchers.correctors import CorrectorBase

class CorrectorYours(CorrectorBase):
    def correct(self, sources: list[str]) -> list[str]:
        hypotheses = sources
        return hypotheses
```

If the corrector aims to (unreasonably) improve existing corrections, use `nice_glitchers.postprocessors.PostProcessorBase`.

```python
from nice_glitchers.postprocessors import PostProcessorBase

class PostProcessorYours(PostProcessorBase):
    def correct(self, sources: list[str], hypotheses: list[str]) -> list[str]:
        return hypotheses
```

### Evaluate the corrector/post_processor performance.

We provide end-to-end evaluation scripts in `experiments/`.

```
cd experiments/
```

Then, you can use `scorer.Scorer` for the evaluation.

For API:
```python
from scorer import Scorer
from nice_glitchers import get_corrector
from nice_glitchers.metrics import LLMSent
import pprint
from gec_metrics import get_metric

metric_ids = ['errant', 'gleu', 'impara', 'pterrant']
# Load metrics that are available from gec-metrics.
metrics = [get_metric(i)() for i in metric_ids]
# If you also use the LLM-based metric:
# metrics.append(
#     LLMSent(LLMSent.Config(
#         organization=os.environ['OPENAI_ORGANIZATION_KEY'],
#         api_key=os.environ['OPENAI_API_KEY'],
#     ))
# )
scorer = Scorer(Scorer.Config(
    metrics=metrics
))
corrector_cls = get_corrector('keepall')  # The corrector to be evaluated
corrector = corrector_cls()
results = scorer.run(corrector)
pprint.pprint(results)
'''Output
{'errant': 0.0,
 'gleu': 0.6390342575052511,
 'impara': 0.5629974568697089,
 'pterrant': 0.0}
'''
```

For CLI:
```sh
python run_exp.py \
    --metrics errant gleu pterrant impara \
    --type corrector \
    --method keepall
```

|Arguments|Description|
|:--|:--|
|--metrics|Which metrics are used. You can make multiple choices from `errant pterrant gleu impara llm`. |
|--type|`corrector` or `postprocessors`.|
|--method|The method id for the --type. You can see the available ids via `nice_glitchers.get_corrector_ids()` and `nice_glitchers.get_postprocessor_ids()`|


This is the end of the tutorial.

# Components of Scorer class

### Loading datasets via gec_datasets.GECDatasets

The target dataset is BEA 2019 development set. You can use this data as follows:
```python
from gec_datasets import GECDatasets
gec = GECDatasets(base_path='exp-datasets/')  # Dataset are stored to the base_path.
bea19_dev = gec.load('bea19-dev')
assert len(bea19_dev.srcs) == 4384
assert len(bea19_dev.refs[0]) == 4384
```

### Metrics

Metrics have the same interface: `.score_sentence()` and `score_corpus()`.

```python
from nice_glitchers import Scorer
from nice_glitchers.corrector import CorrectorKeepAll
from gec_datasets import GECDatasets
from gec_metrics import get_metric
# Load dataset
gec = GECDatasets(base_path='exp-datasets/')  # Dataset are stored to the base_path.
bea19_dev = gec.load('bea19-dev')
# Build corrector
corrector = CorrectorKeepAll()
hyps = [corrector.correct(s) for s in bea19_dev.srcs]
# Evaluate the corrector by GLEU
errant_cls = get_metric('gleu')
metric = errant_cls(errant_cls.Config())
score = metric.score_corpus(
    sources=bea19_dev.srcs,
    hypotheses=hyps,
    references=bea19_dev.refs  # reference based metrics require references
)
print(score)  # output: 0.6390342575052511
```

[gec-metrics](https://github.com/gotutiyan/gec-metrics) covers ERRANT, GLEU, PT-ERRANT, and IMPARA.
```python
from gec_metrics import get_metric

# ERRANT
metric_cls = get_metric('errant')
# GLEU
metric_cls = get_metric('gleu')
# IMPARA
metric_cls = get_metric('impara')
# PTERRANT
metric_cls = get_metric('pterrant')

metric = metric_cls()  # when use the default config.
metric = metric_cls(metric_cls.Config())  # otherwise input the Config.
```

The LLM-based metric is avalilable as `nice_glitchers.metrics.LLMSent`.  
This only supports OpenAI models for now.
```python
from nice_glitchers.metrics import LLMSent
import os
metric = LLMSent(LLMSent.Config(
    organization=os.environ['OPENAI_ORGANIZATION_KEY'],
    api_key=os.environ['OPENAI_API_KEY'],
))
scores = metric.score_sentence(
    sources=['This sentnce contain grammatical error .'],
    hypotheses=['This sentence contains a grammatical error .'],
)
print(scores)
```