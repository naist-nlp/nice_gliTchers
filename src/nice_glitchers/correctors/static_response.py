from .base import CorrectorBase
from dataclasses import dataclass

class CorrectorStaticResponse(CorrectorBase):
    '''This class ignore the input sentence and always return specific response.
    Inspired by https://aclanthology.org/2025.coling-main.331.pdf.
    '''
    @dataclass
    class Config(CorrectorBase.Config):
        response: str = 'Hello'
    
    def correct(self, sources: list[str]) -> list[str]:
        return [self.config.response for _ in sources]