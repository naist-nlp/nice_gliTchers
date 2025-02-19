from .base import CorrectorBase
import random

class CorrectorShuffle(CorrectorBase):
    '''This class always shuffle the input tokens.
    '''
    def correct(self, sources: list[str]) -> list[str]:
        corrected = []
        for s in sources:
            tokens = s.split(" ")
            random.shuffle(tokens)
            corrected.append(" ".join(tokens))
        return corrected