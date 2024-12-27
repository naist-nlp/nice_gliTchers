from .base import CorrectorBase

class CorrectorDeleteAll(CorrectorBase):
    def correct(self, sources: list[str]):
        return ['' for _ in sources]