from .base import CorrectorBase

class CorrectorYours(CorrectorBase):
    def correct(self, sources: list[str]) -> list[str]:
        hypotheses = sources
        return hypotheses