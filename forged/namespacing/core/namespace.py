from typing import Optional

from forged.namespacing.access.context_guard import GlobalContext
from forged.namespacing.core.node import NamespaceNode
from forged.namespacing.core.symbol import Symbol
from forged.namespacing.core.resolver import Resolver
from forged.namespacing.core.utils import split_path


class Namespace:
    def __init__(self, name: str = "root", parent=None, policy=None):
        self.name = name
        self.parent = parent
        self.root = NamespaceNode(name)
        self.resolver = Resolver()
        self.policy = policy  # Optional

    def register(self, path: str, value, **kwargs):
        """Register a symbol at a specific path."""
        parts = split_path(path)
        current = self.root

        for part in parts[:-1]:
            current = current.add_child(part)

        final = parts[-1]

        # Handle conflicts
        if current.has_child(final) and current.get_child(final).symbol:
            self.resolver.handle_conflict(current.get_child(final), value, path)

        node = current.add_child(final)
        node.symbol = value if isinstance(value, Symbol) else Symbol(value=value)

    def resolve(self, path, action: Optional[str] = 'read', context=None, **kwargs):
        """Resolve a path and return the associated symbol."""
        context = context or GlobalContext.get()

        parts = split_path(path)
        current = self.root

        for part in parts:
            current = current.get_child(part)
            if not current:
                raise KeyError(f"Path not found: {path}")

        if current.symbol:
            if action and not current.symbol.check_access(action, context or {}):
                raise PermissionError(f"Access denied: action={action}, path={path}")
            return current.symbol.value

        # Trigger lazy loading if applicable
        if current.symbol is None and self.resolver.has_lazy(path):
            current.symbol = self.resolver.load_lazy(path)

        return current.symbol.value if current.symbol else None

    def resolve_pattern(self, pattern: str):
        """
        Return all symbols matching a wildcard pattern.
        """
        return self.resolver.match_pattern(self.root, pattern)

    def unregister(self, path: str):
        """Remove a symbol at a given path."""
        parts = split_path(path)
        current = self.root
        for part in parts[:-1]:
            current = current.get_child(part)
            if not current:
                raise KeyError(f"Path not found: {path}")
        target = current.get_child(parts[-1])
        if target:
            target.symbol = None

    def list(self, prefix: str = ""):
        """List all registered paths under a prefix."""

        def collect_paths(node, current_path):
            paths = []
            if node.symbol:
                paths.append(current_path)
            for child_name, child_node in node.children.items():
                paths.extend(collect_paths(child_node, f"{current_path}.{child_name}" if current_path else child_name))
            return paths

        parts = split_path(prefix)
        current = self.root
        for part in parts:
            current = current.get_child(part)
            if not current:
                return []

        return collect_paths(current, prefix)

    def to_dict(self, exclude_root: bool = False):
        """Export namespace to dictionary form."""

        def node_to_dict(node):
            data = {}
            if node.symbol:
                data["__symbol__"] = {
                    "name": node.symbol.name,
                    "tags": node.symbol.tags
                }
            for child_name, child_node in node.children.items():
                data[child_name] = node_to_dict(child_node)
            return data

        namespace_dict = node_to_dict(self.root)
        if exclude_root:
            return namespace_dict

        return {self.name: namespace_dict}

    def from_dict(self, data: dict):
        def load_node(node_data, parent_node):
            for key, value in node_data.items():
                if key == "__symbol__":
                    sym_data = value
                    symbol = Symbol(
                        value=None,  # Placeholder — real value may come from plugin
                        name=sym_data.get("name"),
                        tags=sym_data.get("tags", {})
                    )
                    parent_node.symbol = symbol
                    continue

                child_node = parent_node.add_child(key)
                load_node(value, child_node)

        # Assumes one root-level entry
        root_name, root_data = next(iter(data.items()))
        self.name = root_name
        self.root = NamespaceNode(root_name)
        load_node(root_data, self.root)

    def fork(self, name: Optional[str] = None) -> "Namespace":
        """
        Create a forked (composable) copy of this namespace.
        """
        forked = Namespace(name or f"{self.name}_fork", parent=self)

        def resolve_with_fallback(path: str, **kwargs):
            try:
                return forked._resolve_local(path)
            except KeyError:
                if forked.parent:
                    return forked.parent.resolve(path)
                raise

        forked.resolve = resolve_with_fallback
        return forked

    def _resolve_local(self, path: str, **kwargs):
        # Internal: only resolve from this namespace, not parent
        parts = split_path(path)
        current = self.root
        for part in parts:
            current = current.get_child(part)
            if not current:
                raise KeyError(f"Path not found: {path}")
        return current.symbol.value if current.symbol else None

    def __getitem__(self, path: str):
        return self.resolve(path)

    def __setitem__(self, path: str, value):
        self.register(path, value)


