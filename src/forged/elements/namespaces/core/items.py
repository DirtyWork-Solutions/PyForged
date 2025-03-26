"""
This module defines the `Entry` class, which holds and represents an item in a namespace with various attributes
and methods to manage its state and metadata.
"""

from typing import Any, Optional, Dict

from forged.__bases__ import BaseNamespaceItem
from forged.__exceptions__ import NamespacingException


class Entry(BaseNamespaceItem):
    """
    Represents a registered entity (function, class, etc.) with associated metadata.
    """

    def __init__(self, value: Any, name: Optional[str] = None, tags: Optional[Dict[str, Any]] = None,
                 metadata: Optional[dict] = None):
        super().__init__()
        self.value = value
        self.name = name or getattr(value, '__name__', str(value))
        self.tags = tags or {}
        self._frozen = False  # TODO: Implement immutability
        self.metadata = metadata or {}

    def freeze(self):
        self._frozen = True

    def unfreeze(self):
        self._frozen = False

    def is_frozen(self) -> bool:
        return self._frozen


    def get_metadata(self, key: str) -> Any:
        return self.metadata.get(key)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entry):
            return NotImplemented
        return self.name == other.name and self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.name, self.value))

    def __str__(self) -> str:
        return f"NamespaceItem(name={self.name}, value={self.value})"

    def __repr__(self):
        return f"<NamespaceItem name={self.name} frozen={self._frozen} tags={self.tags}>"

