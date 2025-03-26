from __future__ import annotations

from typing import Dict, Optional
from loguru import logger
from dotmap import DotMap
from forged.__bases__ import BaseNamespaceItem


class NamespaceNode:
    def __init__(self, name: str):
        self.name: str = name
        self.entry: BaseNamespaceItem | None = None
        self.children: DotMap = DotMap()

    def add_child(self, name: str) -> BaseNamespaceItem:
        if name not in self.children:
            self.children[name] = NamespaceNode(name)
        return self.children[name]

    def get_child(self, name: str) -> BaseNamespaceItem | None:
        return self.children.get(name)

    def remove_child(self, name: str) -> bool:
        if name in self.children:
            del self.children[name]
            return True
        return False

    def has_child(self, name: str) -> bool:
        return name in self.children

    def find_node_by_path(self, path: str) -> BaseNamespaceItem | None:
        parts = path.split('.')
        current = self
        for part in parts:
            current = current.get_child(part)
            if current is None:
                return None
        return current

    def clone(self) -> 'NamespaceNode':
        clone = NamespaceNode(self.name)
        clone.entry = self.entry  # Shallow copy
        for name, child in self.children.items():
            clone.children[name] = child.clone()
        return clone

    def __repr__(self):
        return f"<NamespaceNode name={self.name} children={list(self.children.keys())}>"

    def __iter__(self):
        return iter(self.children.values())

    def __len__(self):
        return len(self.children)

    def __bool__(self):
        return True

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NamespaceNode):
            return NotImplemented
        return self.name == other.name and dict(self.children) == dict(other.children)

    def __ne__(self, other: object) -> bool:
        return not self == other
