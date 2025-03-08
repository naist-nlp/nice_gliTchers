from .base import PostProcessorBase
from gecommon import CachedERRANT
from gecommon.utils import apply_edits
from dataclasses import dataclass
from gec_metrics import get_metric
import json
from tqdm import tqdm

class PostProcessorAllEditPatterns(PostProcessorBase):
    '''It tries 2^N patterns applied to all edits 
        and select the set of edits with the highest evaluation value.
    '''
    @dataclass
    class Config(PostProcessorBase.Config):
        '''
            - max_edits (int): Ignore a hypothesis that contains more than max_edits edits.
                This is due to a computation cost problem.
            - metric (str): The best edit set will be determined by this metric.
                You can specify from results of `gec_metrics.get_metric_ids()`.
            - model (str): Correction results. This should be in <base_path>/bea19-dev-correction/.
        '''
        max_edits: int = 10
        metric: str = 'impara'
    
    def __init__(self, config: Config = None):
        super().__init__(config)
        self.metric_cls = get_metric(self.config.metric)
        self.metric = self.metric_cls(self.metric_cls.Config())
        self.errant = CachedERRANT()
        self.save_data = []

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.save_data, f, indent=2)
            

    def find_best_edit_pattern(self, src, hyp):
        edits = self.errant.extract_edits(src, hyp)
        num_edits = len(edits)
        # Due to the time complexity of 2^N, we ignore if many edits
        if num_edits >= self.config.max_edits:
            return hyp
        all_pattern_hyps = []
        for edit_set in range(2**num_edits):
            # If i-th bit of `edit_set` is 1, we use i-th edit
            this_edits = [edits[edit_id] for edit_id in range(num_edits)\
                          if (edit_set >> edit_id) & 1]
            this_hyp = apply_edits(src, this_edits)
            all_pattern_hyps.append(this_hyp)
        assert len(set(all_pattern_hyps)) == 2**num_edits
        srcs = [src] * len(all_pattern_hyps)
        scores = self.metric.score_sentence(
            sources=srcs,
            hypotheses=all_pattern_hyps
        )
        # Choose the hyp with the highest score
        best_hyp = sorted(
            list(zip(all_pattern_hyps, scores)),
            key=lambda x: x[1],
        )[-1][0]
        save_data = {
            'src': src,
            'hyp': hyp,
            'best_hyp': best_hyp,
            'index': all_pattern_hyps.index(best_hyp),
            'index-bin': bin(all_pattern_hyps.index(best_hyp)),
            'edits': [str(e) for e in edits],
            'selected_edits': [str(edits[edit_id]) for edit_id in range(num_edits)\
                              if (all_pattern_hyps.index(best_hyp) >> edit_id) & 1],
            'src-score': scores[0],
            'hyp-score': scores[-1],
            'max-score': scores[all_pattern_hyps.index(best_hyp)]
        }
        self.save_data.append(save_data)
        return best_hyp
    
    def correct(
        self,
        sources: list[str],
        hypotheses: list[str]
    ) -> list[str]:
        new_hypotheses = [
            self.find_best_edit_pattern(s, h) for s, h in tqdm(zip(sources, hypotheses))
        ]
        return new_hypotheses