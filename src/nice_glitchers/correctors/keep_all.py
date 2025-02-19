from .base import CorrectorBase

class CorrectorKeepAll(CorrectorBase):
    '''This always keeps the input sentence.
    '''
    def correct(self, sources: list[str]) -> list[str]:
        return sources