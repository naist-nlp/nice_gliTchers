from .base import PostProcessorBase
from gecommon import CachedERRANT
from gecommon.utils import apply_edits
from dataclasses import dataclass
from gec_metrics import get_metric

class PostProcessorOperationFilter(PostProcessorBase):
    '''For GLEU, remove insetion edits and keep deletion and replacement edits.
    '''
    
    def __init__(self, config = None):
        super().__init__(config)
        self.errant = CachedERRANT()

    def filter(self, src, hyp):
        edits = self.errant.extract_edits(src, hyp)
        filtered_edits = [
            e for e in edits if not (e.type[:2] == 'M:' and len(e.c_str.split(' ')) == 1)
        ]
        return apply_edits(src, filtered_edits)
    
    def correct(
        self,
        sources: list[str],
        hypotheses: list[str]
    ) -> list[str]:
        new_hypotheses = [
            self.filter(s, h) for s, h in zip(sources, hypotheses)
        ]
        return new_hypotheses