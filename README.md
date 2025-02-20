# nlp2025-eval-sharedtask-gec
A tools for the shared task regarding hacking Grammatical Error Correction metrics.

# Minimal Installation
```sh
pip install git+https://github.com/naist-nlp/nice_gliTchers
python -m spacy download en_core_web_sm
```
Or
```
git clone https://github.com/naist-nlp/nice_gliTchers
cd nice_gliTchers
pip install -e ./
python -m spacy download en_core_web_sm
```

# Tutorial

### Define your Corrector based on nice_glitchers.correctors.CorrectorBase

`cd experiments/` and create a Python file. Implement your Corrector by inheriting from `CorrectorBase`.

```python
from nice_glitchers.correctors import CorrectorBase

class CorrectorYours(CorrectorBase):
    def correct(self, sources: list[str]) -> list[str]:
        hypotheses = sources
        return hypotheses
```

### Evaluate performance via nice_glitchers.Scorer

This class performs end-to-end evaluation. Basically, all you need is this class.

```python
from nice_glitchers import Scorer
from nice_glitchers.correctors.your_custom_corrector import CorrectorYours
import pprint

scorer = Scorer(Scorer.Config(
    metrics=['errant', 'gleu', 'impara', 'pterrant']
))
corrector_cls = CorrectorYours  # The corrector to be evaluated
corrector = corrector_cls()
results = scorer.run(corrector)
pprint.pprint(results)
'''Output
{'errant': 0.0,
 'gleu': 0.6390342575052511,
 'impara': 0.5629974568697089,
 'pterrant': 0.0}
'''
```

If you want to look more details, you can see the following document.

### Loading datasets via gec_datasets.GECDatasets

The target dataset is BEA 2019 development set. You can use this data as follows:
```python
from gec_datasets import GECDatasets
gec = GECDatasets(base_path='exp-datasets/')  # Dataset are stored to the base_path.
bea19_dev = gec.load('bea19-dev')
assert len(bea19_dev.srcs) == 4384
assert len(bea19_dev.refs[0]) == 4384
```

### Corrector

The Corrector classes are designed for sentence-level processing.

All classes have the same interface: `.correct()`.

```python
from nice_glitchers import Scorer
from nice_glitchers.correctors import CorrectorKeepAll
from gec_datasets import GECDatasets
gec = GECDatasets(base_path='exp-datasets/')  # Dataset are stored to the base_path.
bea19_dev = gec.load('bea19-dev')
corrector = CorrectorKeepAll()
hyps = [corrector.correct(s) for s in bea19_dev.srcs[:10]]
print(hyps)
```

### Metrics

Metrics have the same interface: `.score_sentence()` and `score_corpus()`.

```python
from nice_glitchers import Scorer
from nice_glitchers.corrector import CorrectorKeepAll
from gec_datasets import GECDatasets
from gec_metrics import get_metric
# Load dataset
gec = GECDatasets(base_path='exp-datasets/')  # Dataset are stored to the base_path.
bea19_dev = gec.load('bea19-dev')
# Build corrector
corrector = CorrectorKeepAll()
hyps = [corrector.correct(s) for s in bea19_dev.srcs]
# Evaluate the corrector
errant_cls = get_metric('gleu')
metric = errant_cls(errant_cls.Config())
score = metric.score_corpus(
    sources=bea19_dev.srcs,
    hypotheses=hyps,
    references=bea19_dev.refs  # reference based metrics require references
)
print(score)  # output: 0.6390342575052511
```

[gec-metrics](https://github.com/gotutiyan/gec-metrics) covers ERRANT, GLEU, PT-ERRANT, and IMPARA.
```python
from gec_metrics import get_metric

# ERRANT
metric_cls = get_metric('errant')
# GLEU
metric_cls = get_metric('gleu')
# IMPARA
metric_cls = get_metric('impara')
# PTERRANT
metric_cls = get_metric('pterrant')

metric = metric_cls()  # when use the default config.
metric = metric_cls(metric_cls.Config())  # otherwise input the Config.
```

The LLM-based metric is avalilable as `nice_glitchers.metrics.LLMSent`.  
This only supports OpenAI models for now, and does not support HuggingFace models.
```python
from nice_glitchers.metrics import LLMSent
import os
metric = LLMSent(LLMSent.Config(
    organization=os.environ['OPENAI_ORGANIZATION_KEY'],
    project=os.environ['OPENAI_API_KEY'],
))
scores = metric.score_sentence(
    sources=['This sentnce contain grammatical error .'],
    hypotheses=['This sentence contains a grammatical error .'],
)
print(scores)
```