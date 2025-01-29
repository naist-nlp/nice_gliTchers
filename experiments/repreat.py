from .base import CorrectorBase
from dataclasses import dataclass

class CorrectorRepeat(CorrectorBase):
    '''This class always repeats the input sentence specific times.
    '''
    
    def correct(self, source: str) -> str:
        return source + ' ' + source