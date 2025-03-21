from typing import Dict, Optional

class NamespaceNode:
    def __init__(self, name: str):
        self.name = name
        self.children: Dict[str, 'NamespaceNode'] = {}
        self.symbol = None

    def add_child(self, name: str) -> 'NamespaceNode':
        if name not in self.children:
            self.children[name] = NamespaceNode(name)
        return self.children[name]

    def get_child(self, name: str) -> Optional['NamespaceNode']:
        return self.children.get(name)

    def has_child(self, name: str) -> bool:
        return name in self.children

    def __repr__(self):
        return f"<Node name={self.name} children={list(self.children)}>"
