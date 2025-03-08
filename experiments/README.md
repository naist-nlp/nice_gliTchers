### Evaluate the corrector/post_processor performance

`score.Score` is the class to evaluate corrector/post_processor.  
The evaluation will be done using the BEA-2019 development set by default.

For API:
```python
from scorer import Scorer
from nice_glitchers import get_corrector, get_postprocessor
from nice_glitchers.metrics import LLMSent
import pprint
from gec_metrics import get_metric

metric_ids = ['errant', 'gleu', 'impara', 'pterrant']
# Load metrics that are available from gec-metrics.
metrics = [get_metric(i)() for i in metric_ids]
# If you also use the LLM-based metric:
# metrics.append(
#     LLMSent(LLMSent.Config(
#         model='gpt-4o-mini-2024-07-18',
#         organization=os.environ['OPENAI_ORGANIZATION_KEY'],
#         api_key=os.environ['OPENAI_API_KEY'],
#     ))
# )

# Evaluated on all metrics specified in metrics=.
scorer = Scorer(Scorer.Config(
    metrics=metrics
))
corrector_cls = get_corrector('keepall')  # The corrector to be evaluated
# corrector_cls = get_postprocessor('keepall')  # Postprocessors can also be used.
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

For CLI:
```sh
python run_exp.py \
    --metrics errant gleu pterrant impara \
    --type corrector \
    --method keepall
```

|Arguments|Description|
|:--|:--|
|--metrics|Which metrics are used. You can make multiple choices from `errant pterrant gleu impara llm`. |
|--type|`corrector` or `postprocessors`.|
|--method|The method id for the --type. You can see the available ids via `nice_glitchers.get_corrector_ids()` and `nice_glitchers.get_postprocessor_ids()`|