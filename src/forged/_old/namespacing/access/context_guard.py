import threading
import contextvars

# Thread-local context
_thread_ctx = threading.local()

# Async context (e.g. for FastAPI, asyncio)
_async_ctx = contextvars.ContextVar("pfnaming_context", default={})


class GlobalContext:
    @staticmethod
    def get() -> dict:
        """Return the current combined async/thread context."""
        if hasattr(_thread_ctx, "data"):
            return _thread_ctx.data or _async_ctx.get()
        return _async_ctx.get()

    @staticmethod
    def set(context: dict):
        """Manually override current context."""
        _thread_ctx.data = context
        _async_ctx.set(context)

    @staticmethod
    def update(**kwargs):
        """Merge/update current context with new keys."""
        current = GlobalContext.get()
        updated = {**current, **kwargs}
        GlobalContext.set(updated)

    @staticmethod
    def clear():
        """Clear all scoped context (reset thread + async)."""
        _thread_ctx.data = {}
        _async_ctx.set({})

    @staticmethod
    def scope(**context_overrides):
        """Context manager for temporary scoped context."""
        return _ContextScope(context_overrides)


class _ContextScope:
    def __init__(self, overrides: dict):
        self.overrides = overrides
        self._original = None

    def __enter__(self):
        self._original = GlobalContext.get()
        GlobalContext.update(**self.overrides)

    def __exit__(self, exc_type, exc_val, exc_tb):
        GlobalContext.set(self._original)
