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

from dotmap import DotMap
from loguru import logger
#
def split_path(path: str) -> List[str]:
    """Split a dot path into segments, trimming empty parts."""
    parts = [part for part in path.strip(".").split(".") if part]
    logger.debug(f"{path} was split into {parts}")
    return parts

#
def join_path(parts: Union[str, Tuple]) -> str:
    """Join path parts into a dot path."""
    return ".".join(parts)

#
def is_valid_identifier(name: str):
    """Check if a name is a valid identifier."""
    return name.isidentifier()

#
def merge_tags(*tag_sets: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple tag dictionaries into one, right-biased."""
    merged = {}
    for tags in tag_sets:
        merged.update(tags)
    return merged

# normalize_path: Ensures that a path is in a consistent format.
def normalize_path(path: str) -> str:
    """Normalize a dot path: strip and collapse empty segments."""
    return ".".join([part for part in path.strip(".").split(".") if part])

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


def resolve_dotmap_path(dotmap: DotMap, path: str) -> Any:
    parts = split_path(path)
    current = dotmap
    for part in parts:
        current = current[part]
    return current

def validate_path(path: str) -> bool:
    """
    Strictly validate that a path:
    - Is not empty
    - Has no leading or trailing dots
    - Has no empty segments (e.g. 'a..b')
    - Contains only valid identifiers
    """
    if not path or path.startswith(".") or path.endswith(".") or ".." in path:
        return False

    parts = path.split(".")
    return all(is_valid_identifier(part) for part in parts)
