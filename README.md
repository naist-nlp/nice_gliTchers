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
```

(I will implement PT-ERRANT and GPT-4-based metric ...)

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