from typing import Protocol, Callable, Any, Tuple, Dict, Union, List

# Type aliases
EventArgs = Tuple[Any, ...]
EventKwargs = Dict[str, Any]
EventData = Union[EventArgs, EventKwargs]

# Protocols for interface-like contracts

class ActionLike(Protocol):
    def emit(self, *args: Any, **kwargs: Any) -> None: ...
    def connect(self, handler: Callable[..., Any]) -> None: ...
    def disconnect(self, handler: Callable[..., Any]) -> None: ...

class ActivityLike(Protocol):
    def pipe(self, *operators: Any) -> Any: ...
    def subscribe(self, callback: Callable[[Any], None]) -> Any: ...
