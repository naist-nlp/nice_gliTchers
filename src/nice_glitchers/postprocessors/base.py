import abc
from .utils import CorrectionLoader
from dataclasses import dataclass

class PostProcessorBase(abc.ABC):
    @dataclass
    class Config: ...

    def __init__(self, config=None) -> None:
        self.config = config if config is not None else self.Config()
    
    @abc.abstractmethod
    def correct(
        self,
        sources: list[str],
        hypothesis: list[str]
    ) -> list[str]:
        '''Correct source sentences.

        Args:
            sources (list[str]): Source sentences.
            hypotheses (list[str]): Hypothesis sentences.

        Returns:
            list[str]: (Hacked) corrected sentences.
        '''
        raise NotImplementedError
    
# Template
# from dataclasses import dataclass
# from .base import PostProcessorBase
# class PostProcessorNew(PostProcessorBase):
#     @dataclass
#     class Config(PostProcessorBase.Config): ...
    
#     def __init__(self, config=None) -> None:
#         super().__init__(config)
    
#     def correct(
#         self,
#         sources: list[str],
#         hypothesis: list[str]
#     ) -> list[str]:
#         return None