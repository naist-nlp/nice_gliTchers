# nlp2025-eval-sharedtask-gec
A tools for the shared task regarding hacking Grammatical Error Correction metrics.

# Minimal Installation
```
git clone https://github.com/naist-nlp/nlp2025-eval-sharedtask-gec
cd nlp2025-eval-sharedtask-gec
pip install -e ./
pip install git+https://github.com/gotutiyan/gec-metrics
python -m spacy download en_core_web_sm
```

# Example of the implementation (just example)

- Make `experiments/your_custom_corrector.py`
- Implement your method by inheriting from the `CorrectorBase` class.

This is an example of a Corrector with no editing.

```python
from .base import CorrectorBase

class CorrectorKeepAll(CorrectorBase):
    def correct(self, sources: list[str]):
        # You have to override correct() method for unified interface.
        return sources
```

Then, 

```python
from experiments import Scorer
from experiments.your_custom_corrector import CorrectorKeepAll
import pprint

scorer = Scorer(Scorer.Config(metrics=['errant', 'gleuofficial', 'impara', 'pterrant']))
corrector_cls = CorrectorKeepAll
corrector = corrector_cls(corrector_cls.Config())
results = scorer.run(corrector)
pprint.pprint(results)
'''Output
{'errant': 0.0,
 'gleuofficial': 0.6390342575052511,
 'impara': 0.5629974678184385}
'''
```

You can freely implement `Corrector*` class and easily run the experiments like the above example.

Of course this is just example.


# Implemenation Tips

### Dataset

The target dataset is BEA 2019 development set. You can use this data as follows:
```python
from gec_datasets import GECDatasets
gec = GECDatasets(base_path='datasets/')  # Any path is ok
bea19_dev = gec.load('bea19-dev')
assert len(bea19_dev.srcs) == 4384
assert len(bea19_dev.refs[0]) == 4384
```

### Metrics

The targeted metrics are ERRANT, GLEU, PT-ERRANT, IMPARA, and GPT-4-based one.

The gec-metrics library supports some of them:
```python
from gec_metrics import get_metric

# ERRANT
errant_cls = get_metric('errant')
errant = errant_cls(errant_cls.Config())

# GLEU
gleu_cls = get_metric('gleuofficial')
gleu = gleu_cls(gleu_cls.Config())

# IMPARA
impara_cls = get_metric('impara')
impara = impara_cls(impara_cls.Config())

# PTERRANT
pterrant_cls = get_metric('pterrant')
pterrant = pterrant_cls(pterrant_cls.Config())
```

(LLM-based metric is not implemented yet.)

### Evaluate

Given "hacked" corrected sentences, you can perform evaluation as follows:

```python
from gec_datasets import GECDatasets
from gec_metrcis import get_metric
from gec_metrics.metrics import (
    MetricBaseForReferenceBased,
    MetricBaseForReferenceFree,
)
gec = GECDatasets(base_path='datasets/')
bea19_dev = gec.load('bea19-dev')
hacked_corrections = []

for name in ['errant', 'gleuofficial', 'impara']:
    metric_cls = get_metric(name)
    metric = metric_cls(metric_cls.Config())
    if isinstance(metric, MetricBaseForReferenceBased):
        score = metric.score_corpus(
            sources=bea19_dev.srcs,
            hypotheses=hacked_corrections,
            references=bea19_dev.refs
        )
    elif isinstance(metric, MetricBaseForReferenceFree):
        score = metric.score_corpus(
            sources=bea19_dev.srcs,
            hypotheses=hacked_corrections,
        )
    print(name, score)
```

This way is implemented in `experiments.Score` class.