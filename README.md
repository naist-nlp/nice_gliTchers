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

# Tutorial

### Define your Corrector

`cd experiments/` and create a Python file. Implement your Corrector by inheriting from `CorrectorBase`.

This is a sentence-level processing.

```python
from .base import CorrectorBase

class CorrectorYours(CorrectorBase):
    def correct(self, src: str):
        hyp = src
        return hyp
```

### experiments.Scorer

This class performs end-to-end evaluation. Basically, all you need is this class.

```python
from correctors import Scorer
from correctors.your_custom_corrector import CorrectorYours
import pprint

scorer = Scorer(Scorer.Config(
    metrics=['errant', 'gleuofficial', 'impara', 'pterrant']
))
corrector_cls = CorrectorYours  # The corrector to be evaluated
corrector = corrector_cls()
results = scorer.run(corrector)
pprint.pprint(results)
'''Output
{'errant': 0.0,
 'gleuofficial': 0.6390342575052511,
 'impara': 0.5629974568697089,
 'pterrant': 0.0}
'''
```

If you want to look more details, you can see the following document.

### Dataset

The target dataset is BEA 2019 development set. You can use this data as follows:
```python
from gec_datasets import GECDatasets
gec = GECDatasets(base_path='datasets/')  # Dataset are stored to the base_path.
bea19_dev = gec.load('bea19-dev')
assert len(bea19_dev.srcs) == 4384
assert len(bea19_dev.refs[0]) == 4384
```

### Corrector

The Corrector classes are designed for sentence-level processing.

All classes have the same interface: `.correct()`.

```python
from correctors import Scorer, CorrectorKeepAll
from gec_datasets import GECDatasets
gec = GECDatasets(base_path='datasets/')  # Dataset are stored to the base_path.
bea19_dev = gec.load('bea19-dev')
corrector = CorrectorKeepAll()
hyps = [corrector.correct(s) for s in bea19_dev.srcs[:10]]
print(hyps)
```

### Metrics

Metrics have the same interface: `.score_sentence()` and `score_corpus()`.

```python
from correctors import Scorer, CorrectorKeepAll
from gec_datasets import GECDatasets
from gec_metrics import get_metric
# Load dataset
gec = GECDatasets(base_path='datasets/')  # Dataset are stored to the base_path.
bea19_dev = gec.load('bea19-dev')
# Build corrector
corrector = CorrectorKeepAll()
hyps = [corrector.correct(s) for s in bea19_dev.srcs]
# Evaluate the corrector
errant_cls = get_metric('gleuofficial')
metric = errant_cls(errant_cls.Config())
score = metric.score_corpus(
    sources=bea19_dev.srcs,
    hypotheses=hyps,
    references=bea19_dev.refs  # reference based metrics require references
)
print(score)  # output: 0.6390342575052511
```

The targeted metrics are ERRANT, GLEU, PT-ERRANT, IMPARA, and GPT-4-based one.

The gec-metrics library supports some of them:
```python
from gec_metrics import get_metric

# ERRANT
metric_cls = get_metric('errant')
# GLEU
metric_cls = get_metric('gleuofficial')
# IMPARA
metric_cls = get_metric('impara')
# PTERRANT
metric_cls = get_metric('pterrant')
```

(LLM-based metric is not implemented yet.)