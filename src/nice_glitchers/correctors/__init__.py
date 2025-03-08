from .base import CorrectorBase
from .delete_all import CorrectorDeleteAll
from .keep_all import CorrectorKeepAll
from .static_response import CorrectorStaticResponse
from .knn_search import CorrectorKnnSearch


classes = [
    CorrectorDeleteAll,
    CorrectorKeepAll,
    CorrectorStaticResponse,
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