from .base import CorrectorBase

class CorrectorKeepAll(CorrectorBase):
    def correct(self, source: str) -> str:
        return source