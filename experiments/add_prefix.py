from .base import CorrectorBase
from dataclasses import dataclass

class CorrectorrAddPrefix(CorrectorBase):
    '''This always adds specified prefix to the input sentence.
    Inspired by https://aclanthology.org/2025.coling-main.331.pdf.
    '''
    @dataclass
    class Config(CorrectorBase.Config):
        prefix: str = 'teacher: '
    
    def correct(self, source):
        return self.config.prefix + source