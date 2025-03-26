from contextlib import contextmanager
from copy import deepcopy

@contextmanager
def scoped_override(namespace, overrides: dict):
    """
    Temporarily override values in a namespace within a context.
    Restores previous state after context exits.
    """
    saved = {}
    try:
        for path, value in overrides.items():
            try:
                saved[path] = deepcopy(namespace.resolve(path))
            except KeyError:
                saved[path] = None
            namespace.register(path, value)
        yield namespace
    finally:
        for path, original in saved.items():
            if original is None:
                namespace.unregister(path)
            else:
                namespace.register(path, original)
