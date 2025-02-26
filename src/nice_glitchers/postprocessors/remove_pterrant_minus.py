from dataclasses import dataclass
from .base import PostProcessorBase
from gecommon import CachedERRANT, apply_edits
from gec_metrics import get_metric
class PostProcessorPTERRANTWeight(PostProcessorBase):
    @dataclass
    class Config(PostProcessorBase.Config):
        threshold: float = 0.0125
    
    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.errant = CachedERRANT()
        self.pterrant = get_metric('pterrant')()
    
    def correct(
        self,
        sources: list[str],
        hypothesis: list[str]
    ) -> list[str]:
        num_sents = len(sources)
        hyps = []
        for sent_id in range(num_sents):
            src = sources[sent_id]
            hyp = hypothesis[sent_id]
            hyp_edits = self.errant.extract_edits(src, hyp)
            weights = self.pterrant.calc_edit_weights(
                src, hyp, hyp_edits
            )
            hyp_edits_tuple = [
                (e.o_start, e.o_end, e.c_str) for e in hyp_edits
            ]
            weights = [weights[e] for e in hyp_edits_tuple]
            filtered_edits = [e for i, e in enumerate(hyp_edits) if weights[i] > self.config.threshold]
            new_hyp = apply_edits(src, filtered_edits)
            hyps.append(new_hyp)
        return hyps