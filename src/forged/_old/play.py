from forged.namespacing.registry.composable import CompositeNamespace
from src.forged._old.namespacing import NamespaceNode


class EventLibrary(CompositeNamespace):
    def __init__(self, *namespaces):
        super().__init__(*namespaces, name='events')


class Event(NamespaceNode):
    def __init__(self, name: str):
        super().__init__(name)