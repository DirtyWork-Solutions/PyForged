from forged.elements.namespaces.core.namespace import Namespace
from forged.elements.namespaces.composite import CompositeNamespace

_action_registry = Namespace("actions")
_activity_registry = Namespace("activities")
_listener_registry = Namespace("listeners")
_event_registry = CompositeNamespace(_activity_registry, _activity_registry)

def register_action(name: str, action):
    _action_registry.register(name, action)

def get_action(name: str):
    return _action_registry.resolve(name)

def register_activity(name: str, activity):
    _activity_registry.register(name, activity)

def get_activity(name: str):
    return _activity_registry.resolve(name)

def list_actions():
    return _action_registry.list()

def list_activities():
    return _activity_registry.list()

def register_listener(event_name: str, listener):
    """Register a listener for a specific event."""
    if event_name in _listener_registry:
        _listener_registry.resolve(event_name).append(listener)
    else:
        _listener_registry.register(event_name, [listener])

def emit_event(event_name: str, *args, **kwargs):
    """Emit an event and call all registered listeners."""
    try:
        listeners = _listener_registry.resolve(event_name)
        for listener in listeners:
            listener(*args, **kwargs)
    except KeyError:
        print(f"No listeners registered for event: {event_name}")
