from .base import CorrectorBase

class CorrectorDeleteAll(CorrectorBase):
    '''This class always returns an empty string,
            which means that it always deletes the input.
    '''
    def correct(self, sources: list[str]) -> list[str]:
        return ["" for _ in sources]