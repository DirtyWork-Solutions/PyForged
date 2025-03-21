from typing import Dict, Any


def split_path(path: str):
    """Split a dot path into segments."""
    return path.strip(".").split(".")

def join_path(parts):
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