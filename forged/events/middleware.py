"""

"""
from bedrocked.reporting.reported import logger
from typing import Callable, Any, Dict, Tuple, List

class MiddlewareManager:
    """
    MiddlewareManager manages a list of middleware functions that process events.

    Attributes:
        _middleware (List[Callable]): A list of middleware functions.
    """

    def __init__(self):
        self._middleware: List[Callable[[Any, Any, Dict], Tuple[Any, Any, Dict]]] = []

    def add_middleware(self, middleware: Callable[[Any, Any, Dict], Tuple[Any, Any, Dict]]) -> None:
        """
        Add middleware to the manager.

        :param middleware: **The middleware function to add.**
        """

        if not callable(middleware):
            logger.error(f"'{str(type(middleware))}' is not callable and cannot be used for middleware in events "
                         f"processing or management.")
            raise ValueError("Middleware must be callable")
        self._middleware.append(middleware)

    def remove_middleware(self, middleware: Callable[[Any, Any, Dict], Tuple[Any, Any, Dict]]) -> None:
        """
        Remove middleware from the manager.

        Args:
            middleware (Callable[[Any, Any, Dict], Tuple[Any, Any, Dict]]): The middleware function to remove.
        """
        try:
            self._middleware.remove(middleware)
        except ValueError:
            raise ValueError("Middleware not found in the manager")

    def clear_middleware(self) -> None:
        """
        Clear all middleware from the manager.
        """
        self._middleware.clear()

    def process(self, signal: Any, sender: Any, **kwargs: Dict) -> Tuple[Any, Any, Dict]:
        """
        Process an event through all middleware.

        Args:
            signal (Any): The signal being processed.
            sender (Any): The sender of the signal.
            **kwargs (Dict): Additional arguments to pass to the middleware.

        Returns:
            Tuple[Any, Any, Dict]: The processed signal, sender, and additional arguments.
        """
        for middleware in self._middleware:
            try:
                signal, sender, kwargs = middleware(signal, sender, **kwargs)
            except Exception as e:
                raise RuntimeError(f"Error processing middleware: {e}")
        return signal, sender, kwargs