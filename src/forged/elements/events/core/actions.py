from forged.elements.events.config import get_backend
from forged.elements.events.registry import register_action
from forged.elements.events.core.context import Context
from typing import Callable

class Action:
    """
    Represents a high-level signal/event abstraction.
    Backed by a dispatcher for emitting and connecting event handlers.
    """
    def __init__(self, name: str):
        backend = get_backend("action")

        if backend == "pydispatcher":
            from forged.elements.events.backends.pyd.action_impl import PyDispatcherAction as ActionImpl
        else:
            raise NotImplementedError(f"Unsupported action backend: {backend}")

        self._impl = ActionImpl(name)
        register_action(name, self)

    def emit(self, *args, **kwargs):
        self._impl.emit(*args, **kwargs)

    def connect(self, handler: Callable, ctx: Context = None):
        self._impl.connect(handler)
        if ctx:
            ctx.add_cleanup(lambda: self.disconnect(handler))

    def disconnect(self, handler: Callable):
        self._impl.disconnect(handler)