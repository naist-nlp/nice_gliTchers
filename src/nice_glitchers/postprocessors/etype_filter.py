from .base import PostProcessorBase
from gecommon import CachedERRANT
from gecommon.utils import apply_edits
from dataclasses import dataclass, field
from gec_metrics import get_metric

class PostProcessorEtypeFilter(PostProcessorBase):
    '''For GLEU, remove insetion edits and keep deletion and replacement edits.
    '''

    @dataclass
    class Config(PostProcessorBase.Config):
        filter_type: list[str] = field(
            default_factory=lambda: ['M:']
        )
    
    def __init__(self, config = None):
        super().__init__(config)
        self.errant = CachedERRANT()

    def filter(self, src, hyp):
        edits = self.errant.extract_edits(src, hyp)
        filtered_edits = []
        for e in edits:
            ok = True
            for fil in self.config.filter_type:
                if fil in e.type:
                    ok = False
            if ok:
                filtered_edits.append(e)
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