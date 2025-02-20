from .base import CorrectorBase
from gecommon import CachedERRANT
from gecommon.utils import apply_edits
from dataclasses import dataclass
from gec_metrics import get_metric
from .utils import CorrectionLoader

class CorrectorAllEditPatterns(CorrectorBase):
    '''It tries 2^N patterns applied to all edits 
        and select the set of edits with the highest evaluation value.
    '''
    @dataclass
    class Config(CorrectorBase.Config):
        '''
            - max_edits (int): Ignore a hypothesis that contains more than max_edits edits.
                This is due to a computation cost problem.
            - metric (str): The best edit set will be determined by this metric.
                You can specify from results of `gec_metrics.get_metric_ids()`.
            - model (str): Correction results. This should be in <base_path>/bea19-dev-correction/.
        '''
        max_edits: int = 10
        metric: str = 'impara'
        model: str = 'ens-esc-pillars7'
        base_dir: str = 'datasets/bea19-dev-correction/'
    
    def __init__(self, config: Config = None):
        super().__init__(config)
        self.metric_cls = get_metric(self.config.metric)
        self.metric = self.metric_cls(self.metric_cls.Config())
        self.errant = CachedERRANT()
        self.gec_loader = CorrectionLoader(CorrectionLoader.Config(
            base_dir=self.config.base_dir
        ))

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
        print(scores)
        print()
        # Sort hypotheses by scores
        best_hyp = sorted(
            list(zip(all_pattern_hyps, scores)),
            key=lambda x: x[1],
        )[-1][0]
        return best_hyp
    
    def correct(self, sources: list[str]) -> list[str]:
        hypotheses = self.gec_loader.load(self.config.model)
        new_hypotheses = [
            self.find_best_edit_pattern(s, h) for s, h in zip(sources, hypotheses)
        ]
        return new_hypotheses