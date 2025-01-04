from .base import CorrectorBase

class CorrectorDeleteAll(CorrectorBase):
    def correct(self, source: str) -> str:
        return ""