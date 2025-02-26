from dataclasses import dataclass
from .base import PostProcessorBase
from nice_glitchers.correctors import CorrectorKnnSearch

class PostProcessorKnnSearch(PostProcessorBase):
    @dataclass
    class Config(PostProcessorBase.Config): ...
    
    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.knn_corrector = CorrectorKnnSearch(CorrectorKnnSearch.Config(
            data_ids=['lang8-train', 'troy-1bw', 'troy-blogs'],
            index_dir='exp-datasets/index',
            k=1024
        ))
    
    def correct(
        self,
        sources: list[str],
        hypothesis: list[str]
    ) -> list[str]:
        knn_corrections = self.knn_corrector.correct(sources)
        impara = self.knn_corrector.impara
        num_sents = len(sources)
        new_hyps = []
        for sent_id in range(num_sents):
            scores = impara.score_sentence(
                [sources[sent_id]] * 2,
                [knn_corrections[sent_id], hypothesis[sent_id]]
            )
            if scores[0] > scores[1]:
                new_hyps.append(knn_corrections[sent_id])
            else:
                new_hyps.append(hypothesis[sent_id])
        return new_hyps