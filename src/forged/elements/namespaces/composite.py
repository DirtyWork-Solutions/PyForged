from typing import List, Optional, Any
from forged.elements.namespaces.core.namespace import Namespace
from forged.__exceptions__ import NamespacingException


class CompositeNamespace:
    """
    A composite namespace that aggregates multiple Namespace instances.
    Reads from all, writes to the designated primary namespace.
    """

    def __init__(self, *namespaces: Namespace, write_target: Optional[Namespace] = None):
        if not namespaces:
            raise ValueError("At least one namespace is required")
        self.namespaces: List[Namespace] = list(namespaces)
        self.write_target = write_target or self.namespaces[0]

        if self.write_target not in self.namespaces:
            raise ValueError("Write target must be one of the composite namespaces")

    def resolve(self, path: str, **kwargs) -> Any:
        """Resolve a path from the first namespace that contains it."""
        for ns in self.namespaces:
            try:
                return ns.resolve(path, **kwargs)
            except KeyError:
                continue
        raise KeyError(f"Path '{path}' not found in any namespace.")

    def __contains__(self, path: str) -> bool:
        return any(path in ns for ns in self.namespaces)

    def list(self, prefix: str = '') -> List[str]:
        """List all unique paths across all namespaces."""
        seen = set()
        paths = []
        for ns in self.namespaces:
            for path in ns.list(prefix):
                if path not in seen:
                    seen.add(path)
                    paths.append(path)
        return sorted(paths)

    def __getitem__(self, path: str) -> Any:
        return self.resolve(path)

    def __setitem__(self, path: str, value: Any) -> None:
        """Register into the write target namespace."""
        self.write_target[path] = value

    def unregister(self, path: str) -> None:
        """Unregister from all namespaces where it exists."""
        for ns in self.namespaces:
            if path in ns:
                ns.unregister(path)

    def add_namespace(self, ns: Namespace, write: bool = False):
        """Add a new namespace to the composite.

        :param ns: The namespace to add.
        :param write: Whether to set this namespace as the write target
        """
        if ns not in self.namespaces:
            self.namespaces.append(ns)
        if write:
            self.write_target = ns

    def set_write_target(self, ns: Namespace):
        """Switch the write target namespace."""
        if ns not in self.namespaces:
            raise ValueError("Write target must be part of the composite.")
        self.write_target = ns

    def __str__(self) -> str:
        return f"<CompositeNamespace write_target={self.write_target.name} namespaces={[str(ns) for ns in self.namespaces]}>"

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.list())

    def __len__(self):
        return len(self.list())


if __name__ == '__main__':
    base = Namespace("base")
    plugins = Namespace("plugins")
    local = Namespace("local")

    base.register("foo", 123)
    plugins.register("bar", 456)
    local.register("baz", 789)

    composite = CompositeNamespace(base, plugins, local)

    print(composite.resolve("foo"))  # 123
    print(composite["bar"])  # 456
    print("baz" in composite)  # True
    print(composite.list())  # ['bar', 'baz', 'foo']