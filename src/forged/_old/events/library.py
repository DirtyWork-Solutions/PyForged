from typing import Any, Optional, List
from loguru import logger
from forged.namespacing import Namespace, namespace_from_dict

_events_ns = Namespace('events')


def add_to_library(event: str, value: Any, metadata: Optional[dict] = None) -> None:
    """
    Adds an event to the library.

    Args:
        event (str): The event name.
        value (Any): The value associated with the event.
        metadata (Optional[dict]): Additional metadata for the event.
    """
    try:
        _events_ns.register(path=event, value=value, metadata=metadata or {})
        logger.info(f"Event '{event}' added to library with value: {value} and metadata: {metadata}")
    except Exception as e:
        logger.error(f"Failed to add event '{event}' to library: {e}")


def remove_from_library(event: str) -> None:
    """
    Removes an event from the library.

    Args:
        event (str): The event name to remove.
    """
    try:
        _events_ns.unregister(event)
        logger.info(f"Event '{event}' removed from library")
    except KeyError:
        logger.warning(f"Event '{event}' not found in library")
    except Exception as e:
        logger.error(f"Failed to remove event '{event}' from library: {e}")

def get_from_library(event: str) -> Any:
    """
    Retrieves an event from the library.

    Args:
        event (str): The event name to retrieve.

    Returns:
        Any: The value associated with the event.
    """
    try:
        value = _events_ns.resolve(event)
        logger.info(f"Event '{event}' retrieved from library with value: {value}")
        return value
    except KeyError:
        logger.warning(f"Event '{event}' not found in library")
        return None
    except Exception as e:
        logger.error(f"Failed to retrieve event '{event}' from library: {e}")
        return None

def update_library_event(event: str, value: Any, metadata: Optional[dict] = None) -> None:
    """
    Updates an existing event in the library.

    Args:
        event (str): The event name.
        value (Any): The new value for the event.
        metadata (Optional[dict]): New metadata for the event.
    """
    try:
        if _events_ns.resolve(event):
            _events_ns.register(path=event, value=value, metadata=metadata or {})
            logger.info(f"Event '{event}' updated in library with value: {value} and metadata: {metadata}")
    except KeyError:
        logger.warning(f"Event '{event}' not found in library")
    except Exception as e:
        logger.error(f"Failed to update event '{event}' in library: {e}")

def list_library_events() -> List[str]:
    """
    Lists all events in the library.

    Returns:
        List[str]: A list of all event names in the library.
    """
    try:
        events = _events_ns.list()
        logger.info(f"Listed all events in library: {events}")
        return events
    except Exception as e:
        logger.error(f"Failed to list events in library: {e}")
        return []

if __name__ == '__main__':
    # Example usage
    add_to_library('event1', 'value1', {'description': 'This is event 1'})
    print(_events_ns.to_dict())
    print(get_from_library('event1'))
    update_library_event('event1', 'new_value1', {'description': 'This is the updated event 1'})
    print(get_from_library('event1'))
    print(list_library_events())
    remove_from_library('event1')
    print(get_from_library('event1'))
    print(list_library_events())