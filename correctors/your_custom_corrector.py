from .base import CorrectorBase

class CorrectorYours(CorrectorBase):
    def correct(self, src: str):
        hyp = src
        return hyp