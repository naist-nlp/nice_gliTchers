from dataclasses import dataclass
from .base import PostProcessorBase
from gecommon import CachedERRANT, apply_edits
from gec_metrics import get_metric
class PostProcessorPTERRANTWeight(PostProcessorBase):
    @dataclass
    class Config(PostProcessorBase.Config):
        threshold: float = 0
    
    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.errant = CachedERRANT()
        self.pterrant = get_metric('pterrant')()

    def calc_edit_weights(
        self,
        pterrant,
        src: str,
        ref: str,
        edits
    ) -> list[float]:
        '''This does not take absolute.
        '''
        if edits == []:
            return []
        tuple_edits = [(e.o_start, e.o_end, e.c_str) for e in edits]
        # Remove duplications
        edits = [edits[i] for i, e in enumerate(tuple_edits) if e not in tuple_edits[:i]]
        num_edits = len(edits)
        sents = [pterrant.apply_edits(src, [e]) for e in edits]
        scores1 = pterrant.weight_model.score_sentence([src], [[ref]]) * num_edits
        scores2 = pterrant.weight_model.score_sentence(sents, [[ref] * num_edits])
        weights = [s2 - s1 for s1, s2 in zip(scores1, scores2)]
        return {
            (e.o_start, e.o_end, e.c_str): w for e, w in zip(edits, weights)
        }
    
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
            weights = self.calc_edit_weights(
                self.pterrant, src, hyp, hyp_edits
            )
            hyp_edits_tuple = [
                (e.o_start, e.o_end, e.c_str) for e in hyp_edits
            ]
            weights = [weights[e] for e in hyp_edits_tuple]
            filtered_edits = [e for i, e in enumerate(hyp_edits) if weights[i] > self.config.threshold]
            new_hyp = apply_edits(src, filtered_edits)
            hyps.append(new_hyp)
        return hyps