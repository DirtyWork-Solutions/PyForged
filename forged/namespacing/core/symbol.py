from typing import Any, Optional, Dict

class Symbol:
    def __init__(self, value: Any, name: Optional[str] = None, tags: Optional[Dict[str, Any]] = None):
        self.value = value
        self.name = name or getattr(value, '__name__', None)
        self.tags = tags or {}
        self._frozen = False
        self._metadata = {}

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

    def __repr__(self):
        return f"<Symbol name={self.name} frozen={self._frozen} tags={self.tags}>"

