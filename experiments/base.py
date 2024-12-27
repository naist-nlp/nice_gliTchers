from dataclasses import dataclass, field
from gec_metrics import get_metric
import abc
from gec_datasets import GECDatasets
from gec_metrics.metrics import (
    MetricBaseForReferenceBased,
    MetricBaseForReferenceFree,
)

class CorrectorBase(abc.ABC):
    @dataclass
    class Config: ...

    def __init__(self, config) -> None:
        self.config = config
    
    @abc.abstractmethod
    def correct(self, sources: list[str]) -> list[str]:
        '''Correct source sentences.

        Args:
            sources (list[str]): Source sentences.

        Returns:
            list[str]: (Hacked) corrected sentences.
        '''
        raise NotImplementedError

class Scorer:
    @dataclass
    class Config:
        data_base_path: str = 'datasets/'
        metrics: list = field(default_factory=list)
    
    def __init__(self, config):
        self.config = config
        # print(config)
        gec = GECDatasets(base_path=config.data_base_path)
        self.bea19_dev = gec.load('bea19-dev')
        self.metrics_cls = {
            name: get_metric(name) for name in config.metrics
        }
        self.metric = {
            name: m_cls(m_cls.Config()) for name, m_cls in self.metrics_cls.items()
        }


    def run(self, corrector: CorrectorBase):
        results = dict()
        hypotheses = corrector.correct(self.bea19_dev.srcs)
        for name, metric in self.metric.items():
            if isinstance(metric, MetricBaseForReferenceBased):
                score = metric.score_corpus(
                    sources=self.bea19_dev.srcs,
                    hypotheses=hypotheses,
                    references=self.bea19_dev.refs
                )
            elif isinstance(metric, MetricBaseForReferenceFree):
                score = metric.score_corpus(
                    sources=self.bea19_dev.srcs,
                    hypotheses=hypotheses,
                )
            results[name] = score
        return results


# Template

import argparse

def main(args):
    scorer = Scorer(Scorer.Config())
    corrector = CorrectorBase(CorrectorBase.Config())
    scorer.run(corrector)
    
def get_parser():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_parser()
    main(args)