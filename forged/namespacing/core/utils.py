"""
This module provides utility functions for handling and working with namespaces.

Functions:
    split_path(path: str) -> list:
        Split a dot path into segments.

    join_path(parts: list) -> str:
        Join path parts into a dot path.

    is_valid_identifier(name: str) -> bool:
        Check if a name is a valid identifier.

    merge_tags(*tag_sets: Dict[str, Any]) -> Dict[str, Any]:
        Merge multiple tag dictionaries into one, right-biased.

    normalize_path(path: str) -> str:
        Normalize a dot path to ensure consistent formatting.

    filter_paths(paths: list, prefix: str) -> list:
        Filter a list of paths to include only those with a specific prefix.

    deep_merge_dicts(dict1: dict, dict2: dict) -> dict:
        Recursively merge two dictionaries.

    validate_path(path: str) -> bool:
        Validate that a path conforms to expected rules (e.g., valid identifiers).
"""

from typing import Dict, Any, List, Tuple, Union


def split_path(path: str) -> List[str] | str:
    """Split a dot path into segments."""
    return path.strip(".").split(".")

def join_path(parts: Union[str, Tuple]) -> str:
    """Join path parts into a dot path."""
    return ".".join(parts)

def is_valid_identifier(name: str):
    """Check if a name is a valid identifier."""
    return name.isidentifier()

def merge_tags(*tag_sets: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple tag dictionaries into one, right-biased."""
    merged = {}
    for tags in tag_sets:
        merged.update(tags)
    return merged

# normalize_path: Ensures that a path is in a consistent format.
def normalize_path(path: str) -> str:
    """Normalize a dot path to ensure consistent formatting."""
    return ".".join(part.strip() for part in path.strip(".").split("."))

# filter_paths: Filters a list of paths based on a given prefix.
def filter_paths(paths: list, prefix: str) -> list:
    """Filter a list of paths to include only those with a specific prefix."""
    normalized_prefix = normalize_path(prefix)
    return [path for path in paths if path.startswith(normalized_prefix)]

# deep_merge_dicts: Recursively merges two dictionaries.
def deep_merge_dicts(dict1: dict, dict2: dict) -> dict:
    """Recursively merge two dictionaries."""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    return result

# validate_path: Validates that a path conforms to expected rules.
def validate_path(path: str) -> bool:
    """Validate that a path conforms to expected rules (e.g., valid identifiers)."""
    parts = split_path(path)
    return all(is_valid_identifier(part) for part in parts)