from forged.elements.events.config import get_backend
from forged.elements.events.registry import register_activity
from forged.elements.events.core.context import Context
from typing import Callable

class Activity:
    def __init__(self, source_action):
        backend = get_backend("activity")

        if backend == "rxpy":
            from forged.elements.events.backends.rxp.activity_impl import RxActivity as ActivityImpl
        else:
            raise NotImplementedError(f"Unsupported activity backend: {backend}")

        self._impl = ActivityImpl()
        source_action.connect(lambda *args, **kwargs: self._impl.push((args, kwargs)))
        register_activity(source_action._impl.name, self)

    def pipe(self, *operators):
        return self._impl.pipe(*operators)

    def subscribe(self, callback: Callable, ctx: Context = None):
        sub = self._impl.subscribe(callback)
        if ctx:
            ctx.add_cleanup(lambda: sub.dispose())
        return sub