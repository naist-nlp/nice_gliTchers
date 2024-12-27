from experiments import Scorer
# from experiments import (
#     CorrectorKeepAll,
#     CorrectorDeleteAll
# )
import pprint
from experiments.your_custom_corrector import CorrectorKeepAll

scorer = Scorer(Scorer.Config(metrics=['errant', 'gleuofficial', 'impara']))
corrector_cls = CorrectorKeepAll
corrector = corrector_cls(corrector_cls.Config())
results = scorer.run(corrector)
pprint.pprint(results)
'''Output
{'errant': 0.0,
 'gleuofficial': 0.6390342575052511,
 'impara': 0.5629974678184385}
'''