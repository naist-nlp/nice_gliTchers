from correctors import Scorer
# from experiments import (
#     CorrectorKeepAll,
#     CorrectorDeleteAll
# )
import pprint
from correctors.your_custom_corrector import CorrectorYours

scorer = Scorer(Scorer.Config(metrics=['errant', 'gleuofficial', 'impara', 'pterrant']))
corrector_cls = CorrectorYours
corrector = corrector_cls()
results = scorer.run(corrector)
pprint.pprint(results)
'''Output
{'errant': 0.0,
 'gleuofficial': 0.6390342575052511,
 'impara': 0.5629974568697089,
 'pterrant': 0.0}
'''