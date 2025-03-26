from typing import Dict, Optional
from loguru import logger

from forged.__bases__ import BaseSymbol


class NamespaceNode:
    def __init__(self, name: str):
        """
        Initialize a NamespaceNode.

        Args:
            name (str): The name of the node.
        """
        self.name: str = name
        self.children: Dict[str, 'NamespaceNode'] = {}
        self.symbol: Optional[BaseSymbol] = None

    def add_child(self, name: str) -> 'NamespaceNode':
        """
        Add a child node.

        Args:
            name (str): The name of the child node.

        Returns:
            NamespaceNode: The added child node.
        """
        if name not in self.children:
            self.children[name] = NamespaceNode(name)
        return self.children[name]

    def get_child(self, name: str) -> Optional['NamespaceNode']:
        """
        Get a child node by name.

        Args:
            name (str): The name of the child node.

        Returns:
            Optional[NamespaceNode]: The child node if it exists, otherwise None.
        """
        return self.children.get(name)

    def remove_child(self, name: str) -> bool:
        """
        Remove a child node by name.

        Args:
            name (str): The name of the child node to remove.

        Returns:
            bool: True if the child was removed, False if it did not exist.
        """
        if name in self.children:
            del self.children[name]
            return True
        return False

    def has_child(self, name: str) -> bool:
        """
        Check if a child node exists.

        Args:
            name (str): The name of the child node.

        Returns:
            bool: True if the child node exists, otherwise False.
        """
        return name in self.children

    def find_node_by_path(self, path: str) -> Optional['NamespaceNode']:
        """
        Find a node by a given path.

        Args:
            path (str): The path to the node.

        Returns:
            Optional[NamespaceNode]: The node if found, otherwise None.
        """
        parts = path.split('.')
        current_node = self
        for part in parts:
            current_node = current_node.get_child(part)
            if current_node is None:
                return None
        return current_node

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NamespaceNode):
            return NotImplemented
        return self.name == other.name and self.children == other.children

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __len__(self) -> int:
        return len(self.children)

    def __iter__(self):
        return iter(self.children.values())

    def __repr__(self) -> str:
        """
        Return a string representation of the node.

        Returns:
            str: The string representation of the node.
        """
        return f"<Node name={self.name} children={list(self.children)}>"
