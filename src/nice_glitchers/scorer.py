from dataclasses import dataclass, field
from gec_datasets import GECDatasets
from gec_metrics import get_metric
from gec_metrics.metrics import (
    MetricBase,
    MetricBaseForReferenceBased,
    MetricBaseForReferenceFree,
    MetricBaseForSourceFree,
)
from .correctors import CorrectorBase
class Scorer:
    @dataclass
    class Config:
        data_base_path: str = 'exp-datasets/'
        data_id: str = 'bea19-dev'
        metrics: list = field(default_factory=list)
    
    def __init__(self, config):
        self.config = config
        gec = GECDatasets(base_path=config.data_base_path)
        self.data = gec.load(self.config.data_id)
        for m in self.config.metrics:
            # All metrics must inherit from gec_metrics.metrics.MetricBase.
            assert isinstance(m, MetricBase)
        self.metrics = {
            m.__class__.__name__: m for m in self.config.metrics
        }

    def run(self, corrector: CorrectorBase):
        results = dict()
        hypotheses = corrector.correct(self.data.srcs)
        for name, metric in self.metrics.items():
            if isinstance(metric, MetricBaseForReferenceBased):
                score = metric.score_corpus(
                    sources=self.data.srcs,
                    hypotheses=hypotheses,
                    references=self.data.refs
                )
            elif isinstance(metric, MetricBaseForReferenceFree):
                score = metric.score_corpus(
                    sources=self.data.srcs,
                    hypotheses=hypotheses,
                )
            elif isinstance(metric, MetricBaseForSourceFree):
                score = metric.score_corpus(
                    hypotheses=hypotheses,
                    references=self.data.refs
                )
            results[name] = score
        return results