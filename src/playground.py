from forged.elements.namespaces.named import Namespace, CompositeNamespace
from forged.elements.events.decorators import on_action, on_activity
from forged.elements.events.registry import _activity_registry, _action_registry

events = Namespace('events')
global_namespace = CompositeNamespace()
global_namespace.add_namespace(events)