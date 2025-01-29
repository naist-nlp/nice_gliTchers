from .base import CorrectorBase
import random

class CorrectorShuffle(CorrectorBase):
    '''This class always shuffle the input tokens.
    '''
    def correct(self, source: str) -> str:
        tokens = source.split(" ")
        random.shuffle(tokens)
        return " ".join(tokens)