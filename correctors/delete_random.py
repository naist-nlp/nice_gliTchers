from .base import CorrectorBase
from dataclasses import dataclass
import random

class CorrectorDeleteRandom(CorrectorBase):
    '''This class deletes a part of input sentence.
    For each token, we delete it with "ratio" probability.
    '''
    @dataclass
    class Config(CorrectorBase.Config):
        ratio: float = 0.5

    def correct(self, sources: list[str]) -> list[str]:
        corrected = []
        for s in sources:
            tokens = s.split()
            new_tokens = []
            for t in tokens:
                sample_int = random.randint(0, 100)
                if sample_int < 100 * self.config.ratio:
                    new_tokens.append(t)
            corrected.append(" ".join(new_tokens))
        assert len(corrected) == len(sources)
        return corrected