import abc
from .base import PostProcessorBase
from .utils import CorrectionLoader
from dataclasses import dataclass

class PostProcessorKeepAll(PostProcessorBase):
    def __init__(self, config=None) -> None:
        self.config = config if config is not None else self.Config()
    
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
        return hypothesis