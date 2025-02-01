from .base import CorrectorBase
from dataclasses import dataclass

class CorrectorRepeat(CorrectorBase):
    '''This class always repeats the input sentence specific times.
    '''
    def correct(self, sources: list[str]) -> list[str]:
        return [s + ' ' + s for s in sources]