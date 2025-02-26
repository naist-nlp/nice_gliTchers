from .base import PostProcessorBase
from .all_edit_patterns import PostProcessorAllEditPatterns
from .operation_filter import PostProcessorOperationFilter
from .keep_all import PostProcessorKeepAll
from .remove_pterrant_minus import PostProcessorPTERRANTWeight
from .knn_search import PostProcessorKnnSearch

classes = [
    PostProcessorAllEditPatterns,
    PostProcessorOperationFilter,
    PostProcessorKeepAll,
    PostProcessorPTERRANTWeight,
    PostProcessorKnnSearch
]
id2class = {
    c.__name__.lower().replace('postprocessor', ''): c for c in classes
}

def get_postprocessor_ids():
    return list(id2class.keys())

def get_postprocessor(name=None):
    if name not in get_postprocessor_ids():
        raise ValueError(f'The name {name} is invalid. Candidates are {get_postprocessor_ids()}.')
    return id2class[name]