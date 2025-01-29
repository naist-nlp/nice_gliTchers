from .base import CorrectorBase

class CorrectorKeepAll(CorrectorBase):
    '''This always keeps the input sentence.
    '''
    def correct(self, source: str) -> str:
        return source