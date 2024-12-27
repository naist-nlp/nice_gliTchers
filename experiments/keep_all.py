from .base import CorrectorBase

class CorrectorKeepAll(CorrectorBase):
    def correct(self, sources: list[str]):
        return sources