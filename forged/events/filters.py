"""
Event filtering module for the Runecaller application.

This module defines classes to create and manage event filters.
"""

from typing import Callable, Any, Dict, List

class EventFilter:
    """
    EventFilter class to define and apply filters to events.

    Attributes:
        _condition (Callable[[Any, Any, Dict], bool]): The condition function to apply as a filter.
    """

    def __init__(self, condition: Callable[[Any, Any, Dict], bool]):
        """
        Initialize an EventFilter with a condition function.

        Args:
            condition (Callable[[Any, Any, Dict], bool]): The condition function to apply as a filter.
        """
        self._condition = condition

    def apply(self, signal: Any, sender: Any, **kwargs: Dict) -> bool:
        """
        Apply the filter to an event.

        Args:
            signal (Any): The signal being processed.
            sender (Any): The sender of the signal.
            **kwargs (Dict): Additional arguments to pass to the filter.

        Returns:
            bool: True if the event passes the filter, False otherwise.
        """
        return self._condition(signal, sender, **kwargs)

class EventFilterManager:
    """
    EventFilterManager class to manage and apply multiple event filters.

    Attributes:
        _filters (List[EventFilter]): A list of event filters.
    """

    def __init__(self):
        """
        Initialize an EventFilterManager with an empty list of filters.
        """
        self._filters: List[EventFilter] = []

    def add_filter(self, event_filter: EventFilter) -> None:
        """
        Add a filter to the manager.

        Args:
            event_filter (EventFilter): The filter to add.
        """
        self._filters.append(event_filter)

    def remove_filter(self, event_filter: EventFilter) -> None:
        """
        Remove a filter from the manager.

        Args:
            event_filter (EventFilter): The filter to remove.
        """
        self._filters.remove(event_filter)

    def apply_filters(self, signal: Any, sender: Any, **kwargs: Dict) -> bool:
        """
        Apply all filters to an event.

        Args:
            signal (Any): The signal being processed.
            sender (Any): The sender of the signal.
            **kwargs (Dict): Additional arguments to pass to the filters.

        Returns:
            bool: True if the event passes all filters, False otherwise.
        """
        return all(event_filter.apply(signal, sender, **kwargs) for event_filter in self._filters)