from src.forged._old.namespacing import Symbol
from forged.namespacing.registry.composable import CompositeNamespace, merge_namespaces

__all__ = [
    "Namespace",
    "Symbol",
    "CompositeNamespace",
    "merge_namespaces",
    'register',
    "bind_class_methods",
    "split_path",
    "join_path",
    "filter_paths",
    "normalize_path",
    "validate_path",
    "deep_merge_dicts"
]
