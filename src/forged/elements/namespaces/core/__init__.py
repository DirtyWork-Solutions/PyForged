"""
TODO: Add module docs
""""""
This module initializes the core components of the namespace system, including the `Namespace`, `NamespaceNode`, `Entry`, and `Resolver` classes.

Classes:
    - Namespace: Manages a collection of symbols organized in a hierarchical structure.
    - NamespaceNode: Represents a node in a hierarchical namespace structure.
    - Entry: Represents a registered entity (function, class, etc.) with associated metadata.
    - Resolver: Handles conflicts and lazy loading within the namespace.
"""

from forged.elements.namespaces.core.namespace import Namespace
from forged.elements.namespaces.core.nodes import NamespaceNode
from forged.elements.namespaces.core.items import Entry
from forged.elements.namespaces.core.resolver import Resolver

__all__ = ["Namespace", "NamespaceNode", "Entry", "Resolver"]