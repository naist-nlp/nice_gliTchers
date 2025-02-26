from .base import CorrectorBase
from .add_prefix import CorrectorrAddPrefix
from .delete_all import CorrectorDeleteAll
from .delete_random import CorrectorDeleteRandom
from .keep_all import CorrectorKeepAll
from .shuffle import CorrectorShuffle
from .static_response import CorrectorStaticResponse
from .repreat import CorrectorRepeat
from .knn_search import CorrectorKnnSearch


classes = [
    CorrectorrAddPrefix,
    CorrectorDeleteAll,
    CorrectorDeleteRandom,
    CorrectorShuffle,
    CorrectorKeepAll,
    CorrectorStaticResponse,
    CorrectorRepeat,
    CorrectorKnnSearch
]
id2class = {
    c.__name__.lower().replace('corrector', ''): c for c in classes
}

def get_corrector_ids():
    return list(id2class.keys())

def get_corrector(name=None):
    if name not in get_corrector_ids():
        raise ValueError(f'The name {name} is invalid. Candidates are {get_corrector_ids()}.')
    return id2class[name]