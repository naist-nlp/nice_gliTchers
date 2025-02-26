from dataclasses import dataclass, field
from gec_datasets import GECDatasets
from gec_metrics.metrics import (
    MetricBase,
    MetricBaseForReferenceBased,
    MetricBaseForReferenceFree,
    MetricBaseForSourceFree,
)
from nice_glitchers.correctors import CorrectorBase
from nice_glitchers.postprocessors import PostProcessorBase
from pathlib import Path

class Scorer:
    @dataclass
    class Config:
        hyp_path: str = "exp-datasets/bea19-dev-correction/gector-3sys-voting.txt"
        dataset_dir: str = 'exp-datasets'
        data_id: str = 'bea19-dev'
        outdir: str = 'exp-outputs/'
        metrics: list = field(default_factory=list)
    
    def __init__(self, config):
        self.config = config
        # Load sources and references
        gec = GECDatasets(base_path=config.dataset_dir)
        self.data = gec.load(self.config.data_id)
        # Load hypotheses for PostProcessor*
        self.hyps = open(self.config.hyp_path).read().rstrip().split('\n')
        for m in self.config.metrics:
            # All metrics must inherit from gec_metrics.metrics.MetricBase.
            assert isinstance(m, MetricBase)
        self.metrics = {
            m.__class__.__name__: m for m in self.config.metrics
        }

    def run(self, corrector):
        results = dict()
        # Obtain "hacked" corrections
        if isinstance(corrector, PostProcessorBase):
            hypotheses = corrector.correct(
                self.data.srcs,
                self.hyps
            )
        elif isinstance(corrector, CorrectorBase):
            hypotheses = corrector.correct(self.data.srcs)
        else:
            raise ValueError(f'corrector should be an instance of CorectorBase or PostProcessorBase.')
        save_dir = Path(self.config.outdir) / corrector.__class__.__name__.lower()
        save_dir.mkdir(exist_ok=True, parents=True)
        save_path = save_dir / (self.config.data_id + '.out')
        save_path.write_text('\n'.join(hypotheses))
        # Evaluate the hypotheses
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