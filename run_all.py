from correctors import Scorer
import correctors
import inspect
import pprint
from pathlib import Path
import json

def get_corrector_ids() -> list[str]:
    '''Generate a list of ids with the class name in lower case.
    '''
    ids = [
        elem[0].lower() for elem in inspect.getmembers(correctors, inspect.isclass) \
            if elem[0].lower().startswith('corrector') and not elem[0].lower().startswith('correctorbase')
    ]
    return ids

def get_corrector(_id: str):
    '''Generate a dictionary of ids and classes with the class name in lower case as the key.
    '''
    if not _id in get_corrector_ids():
        raise ValueError(f'The metric_id should be {get_corrector_ids()}. Your input is {_id}.')
    metric_dict = {
        elem[0].lower(): elem[1] for elem in inspect.getmembers(correctors, inspect.isclass) \
              if elem[0].lower().startswith('corrector')
    }
    return metric_dict[_id]

scorer = Scorer(Scorer.Config(metrics=['errant', 'gleuofficial', 'impara', 'pterrant']))
for _id in get_corrector_ids():
    corrector = get_corrector(_id)()
    results = scorer.run(corrector)
    print(f'=== Corrector id: {_id} ===')
    pprint.pprint(results)
    save_dir = Path('exp-outputs/')
    save_dir.mkdir(exist_ok=True)
    save_path = save_dir / (_id + '.json')
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2)