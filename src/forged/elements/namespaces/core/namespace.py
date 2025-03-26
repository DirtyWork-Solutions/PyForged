"""
TODO: Namespace Module Doc String
"""

from typing import Any, List, Optional, Tuple

from forged.__bases__ import BaseNamespace, BaseNamespaceItem
from forged.elements.namespaces.aliasing import Aliaser
from forged.elements.namespaces.core.items import Entry
from forged.elements.namespaces.core.nodes import NamespaceNode
from forged.elements.namespaces.core.resolver import Resolver
from forged.elements.namespaces.utils import split_path

from loguru import logger


class Namespace(BaseNamespace):
    """
    Manages a collection of symbols organized in a hierarchical structure
    """

    def __init__(self, name: Optional[str] = None, parent: Optional['Namespace'] = None, **kwargs):
        super().__init__(name or '')
        self.parent = parent
        self.root = NamespaceNode('')  # ✅ Always unnamed root for internal traversal
        self.resolver = Resolver()
        self.aliaser = Aliaser()

    def register(self, path: str, value: Any, metadata: Optional[dict] = None, **kwargs) -> None:
        parts = split_path(path)
        current = self.root

        for part in parts[:-1]:
            current = current.add_child(part)

        final = parts[-1]

        if current.has_child(final) and current.get_child(final).entry:
            self.resolver.handle_conflict(current.get_child(final), value, path)

        node = current.add_child(final)
        node.entry = Entry(value=value, metadata=metadata)

    def resolve(self, path: str, action: Optional[str] = 'read', context: Optional[Any] = None, **kwargs) -> Any:
        path = self.aliaser.resolve_path(path)

        parts = split_path(path)
        current = self.root
        for i, part in enumerate(parts):
            next_node = current.get_child(part)
            if next_node is None:
                if self.resolver.has_lazy(path):
                    next_node = current.add_child(part)
                else:
                    raise KeyError(f"Path not found: {'.'.join(parts[:i + 1])}")
            current = next_node

        if current.entry is None and self.resolver.has_lazy(path):
            current.entry = self.resolver.load_lazy(path)

        if current.entry is None:
            raise KeyError(f"Entry not found at: {path}")

        if isinstance(current.entry, list) and context:
            # Select based on metadata
            return self.resolver.resolve_with_context(current.entry, context)

        return current.entry.value

    def resolve_pattern(self, pattern: str) -> list[tuple[str, BaseNamespaceItem]]:
        """
        Return all entries matching a wildcard pattern.
        """
        return self.resolver.match_pattern(self.root, pattern)

    def unregister(self, path: str) -> None:
        """Remove an entry at a given path."""
        parts = split_path(path)
        current = self.root
        for part in parts[:-1]:
            current = current.get_child(part)
            if not current:
                raise KeyError(f"Path not found: {path}")
        # Remove the node from the parent's children entirely.
        if parts[-1] in current.children:
            del current.children[parts[-1]]
            logger.success(f"Unregistered Namespace: {path}")
        else:
            raise KeyError(f"Path not found: {path}")

    def add_alias(self, alias: str, target: str):
        self.aliaser.add(alias, target)

    def remove_alias(self, alias: str):
        self.aliaser.remove(alias)

    def list_aliases(self) -> dict:
        return self.aliaser.all()

    def list(self, prefix: str = '') -> List[str]:
        def collect_paths(node: NamespaceNode | BaseNamespaceItem, current_path: str) -> List[str]:
            paths = []
            if node.entry:
                paths.append(current_path)
            for child_name in node.children:
                new_path = f"{current_path}.{child_name}" if current_path else child_name
                paths.extend(collect_paths(node.children[child_name], new_path))
            return paths

        if prefix:
            parts = split_path(prefix)
            current = self.root
            for part in parts:
                current = current.get_child(part)
                if not current:
                    return []
            return collect_paths(current, prefix)
        else:
            return collect_paths(self.root, '')

    def to_dict(self, exclude_root: bool = False) -> dict:
        """Export namespace to dictionary form."""

        def node_to_dict(node):
            data = {}
            if node.entry:
                data['__entry__'] = {
                    'name': node.entry.value,
                    'tags': node.entry.metadata if node.entry.metadata else {}
                }
            for child_name, child_node in node.children.items():
                data[child_name] = node_to_dict(child_node)
            return data

        namespace_dict = node_to_dict(self.root)
        if exclude_root:
            return namespace_dict

        return {self.name: namespace_dict}

    def from_dict(self, data: dict) -> None:
        def load_node(node_data: dict, parent_node: NamespaceNode | BaseNamespaceItem) -> None:
            for key, value in node_data.items():
                if key == '__entry__':
                    sym_data = value
                    item = Entry(
                        value=sym_data.get('name'),
                        metadata=sym_data.get('tags', {})
                    )
                    parent_node.entry = item
                    continue

                child_node = parent_node.add_child(key)
                load_node(value, child_node)

        # Assumes one root-level entry
        root_name, root_data = next(iter(data.items()))
        self.__init__(root_name)
        load_node(root_data, self.root)

    def _resolve_local(self, path: str, **kwargs) -> Any:
        # Internal: only resolve from this namespace, not parent
        parts = split_path(path)
        current = self.root
        for part in parts:
            current = current.get_child(part)
            if not current:
                raise KeyError(f"Path not found: {'.'.join(parts[:parts.index(part) + 1])}")
        return current.entry.value if current.entry else None

    def __getitem__(self, path: str) -> Any:
        return self.resolve(path)

    def __setitem__(self, path: str, value: Any) -> None:
        logger.debug(f"Registering {path} -> {value} in {self.name}")
        self.register(path, value)

    def __repr__(self) -> str:
        return f"<Namespace(name={self.name})>"

    def __str__(self) -> str:
        return self.name

    def __len__(self) -> int:
        return len(self.list())

    def __contains__(self, path: str) -> bool:
        try:
            self.resolve(path)
            return True
        except KeyError:
            return False

    def __iter__(self):
        return iter(self.list())


if __name__ == '__main__':
    ns = Namespace("models")

    ns.register("v1.0.embed", lambda: "old")
    ns.register("v2.0.embed", lambda: "new")

    ns.add_alias("latest", "v2.0.embed")

    print(ns.resolve("latest")())  # 👉 "new"
    print(ns["latest"]())  # 👉 "new"

    ns.add_alias("default", "v1.0.embed")
