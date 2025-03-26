from contextlib import contextmanager
from typing import List, Callable

class Context:
    """
    Collects cleanup callbacks to run at the end of a context.
    Useful for managing temporary subscriptions or connections.
    """
    def __init__(self):
        self._cleanups: List[Callable[[], None]] = []

    def add_cleanup(self, cleanup_fn: Callable[[], None]):
        self._cleanups.append(cleanup_fn)

    def cleanup(self):
        for fn in self._cleanups:
            try:
                fn()
            except Exception:
                pass
        self._cleanups.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()


# Convenience contextmanager
@contextmanager
def scoped_context():
    ctx = Context()
    yield ctx
    ctx.cleanup()

