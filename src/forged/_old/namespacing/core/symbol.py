from typing import Any, Optional, Dict

from forged.__bases__ import BaseSymbol
from forged.namespacing.access.acl import ACL

class Symbol(BaseSymbol):
    def __init__(self,
                 value: Any,
                 name: Optional[str] = None,
                 tags: Optional[Dict[str, Any]] = None,
                 acl=None,
                 metadata: Optional[dict] = None):
        self.acl = None
        self.value = value
        self.name = name or getattr(value, '__name__', None)
        self.tags = tags or {}
        self._frozen = False
        self._metadata = metadata or {}
        self.acl = acl or ACL()  # optional

    @property
    def metadata(self):
        return self._metadata

    def check_access(self, action: str, context: dict) -> bool:
        if self.acl:
            return self.acl.check(action, context)
        return True

    def freeze(self):
        self._frozen = True

    def is_frozen(self) -> bool:
        return self._frozen

    def attach_metadata(self, key: str, value: Any):
        if self._frozen:
            raise ValueError("Cannot modify a frozen symbol.")
        self._metadata[key] = value

    def get_metadata(self, key: str) -> Any:
        return self._metadata.get(key)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Symbol):
            return NotImplemented
        return self.name == other.name and self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.name, self.value))

    def __str__(self) -> str:
        return f"Symbol(name={self.name}, value={self.value})"

    def __repr__(self):
        return f"<Symbol name={self.name} frozen={self._frozen} tags={self.tags}>"

