from dataclasses import dataclass
import abc

class CorrectorBase(abc.ABC):
    @dataclass
    class Config: ...

    def __init__(self, config=None) -> None:
        self.config = config if config is not None else self.Config()
    
    @abc.abstractmethod
    def correct(self, sources: list[str]) -> list[str]:
        '''Correct source sentences.

        Args:
            sources (list[str]): Source sentences.

        Returns:
            list[str]: (Hacked) corrected sentences.
        '''
        raise NotImplementedError


# Template
# from .base import CorrectorBase
# from dataclasses import dataclass
# class CorrectorNew(CorrectorBase):
#     @dataclass
#     class Config(CorrectorBase.Config): ...

#     def __init__(self, config=None) -> None:
#         self.config = config if config is not None else self.Config()
    
#     def correct(self, sources: list[str]) -> list[str]:
#         '''Correct source sentences.

#         Args:
#             sources (list[str]): Source sentences.

#         Returns:
#             list[str]: (Hacked) corrected sentences.
#         '''
#         raise NotImplementedError