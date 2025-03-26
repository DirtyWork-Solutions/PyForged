"""
This module provides the **CompositeNamespace** class, which allows for the management of multiple namespaces
with layered priorities and read-only options. It supports resolving paths, registering values, and mounting
sub-namespaces under specific prefixes.

**Classes:**
    - CompositeNamespace: *Manages multiple namespaces with layered priorities and read-only options.*
"""

from forged.__bases__ import BaseNamespace


class CompositeNamespace(BaseNamespace):
    """
    This class manages multiple namespaces with layered priorities and read-only options. It supports resolving paths,
    registering values, and mounting sub-namespaces under specific prefixes.

    Attributes:
        name (str): The name of the composite namespace.
        layers (list): A list of tuples containing (namespace, read_only, priority).

    Methods:
        __init__(*namespaces, name="composite"): Initializes the CompositeNamespace with optional namespaces.
        _sorted_layers(): Returns the layers sorted by priority in descending order.
        resolve(path: str, **kwargs): Resolves a path across all layers.
        resolve_all(path: str): Resolves a path across all layers and returns all matches.
        register(path: str, value, layer: int = 0, **kwargs): Registers a value in a specific layer.
        append_layer(ns, read_only=False, priority=100): Appends a namespace layer.
        add_layer(ns, position=0, read_only=False, priority=100): Adds a namespace layer at a specific position.
        set_layer_priority(ns, new_priority: int): Sets the priority of a specific namespace layer.
        remove_layer(ns): Removes a namespace layer.
        list(path_prefix: str = ""): Lists all paths with a specific prefix across all layers.
        list_layers(): Lists all layers with their attributes.
        resolve_pattern(pattern: str): Resolves a pattern across all layers.
        mount(mount_path: str, sub_namespace): Mounts a sub-namespace under a specific prefix.
    """

    def __init__(self, *namespaces, name="composite"):
        """
        Initializes the CompositeNamespace with optional namespaces.

        Args:
            *namespaces: Optional namespaces to initialize with.
            name (str): The name of the composite namespace. Defaults to "composite".
        """
        self.name = name
        self.layers = []  # list of (namespace, read_only, priority)
        for ns in namespaces:
            self.append_layer(ns)

    def _sorted_layers(self):
        """
        Returns the layers sorted by priority in descending order.

        Returns:
            list: Sorted layers by priority.
        """
        return sorted(self.layers, key=lambda item: item[2], reverse=True)

    def has_path(self, path: str) -> bool:
        """
        Checks if a path exists in any of the layers.

        Args:
            path (str): The path to check.

        Returns:
            bool: True if the path exists in any layer, False otherwise.
        """
        for ns, _, _ in self._sorted_layers():
            if ns.has_path(path):
                return True
        return False

    def resolve(self, path: str, **kwargs):
        """
        Resolves a path across all layers.

        Args:
            path (str): The path to resolve.
            **kwargs: Additional arguments for resolution.

        Returns:
            Any: The resolved value.

        Raises:
            KeyError: If the path is not found in any layer.
        """
        for ns, _, _ in self._sorted_layers():
            try:
                return ns.resolve(path, **kwargs)
            except KeyError:
                continue
        raise KeyError(f"Path not found in composite: {path}")

    def resolve_all(self, path: str):
        """
        Resolves a path across all layers and returns all matches.

        Args:
            path (str): The path to resolve.

        Returns:
            list: All resolved values.
        """
        results = []
        for ns, _, _ in self._sorted_layers():
            try:
                results.append(ns.resolve(path))
            except KeyError:
                continue
        return results

    def register(self, path: str, value, layer: int = 0, **kwargs):
        """
        Registers a value in a specific layer.

        Args:
            path (str): The path to register.
            value: The value to register.
            layer (int): The layer index to register in. Defaults to 0.
            **kwargs: Additional arguments for registration.

        Raises:
            IndexError: If the layer index is out of bounds.
            PermissionError: If the layer is read-only.
        """
        if layer >= len(self.layers):
            raise IndexError(f"Layer index {layer} out of bounds")
        ns, read_only, _ = self.layers[layer]
        if read_only:
            raise PermissionError(f"Cannot register in read-only layer: {ns.name}")
        ns.register(path, value, **kwargs)

    def append_layer(self, ns, read_only=False, priority=100):
        """
        Appends a namespace layer.

        Args:
            ns: The namespace to append.
            read_only (bool): Whether the layer is read-only. Defaults to False.
            priority (int): The priority of the layer. Defaults to 100.
        """
        self.layers.append((ns, read_only, priority))

    def add_layer(self, ns, position=0, read_only=False, priority=100):
        """
        Adds a namespace layer at a specific position.

        Args:
            ns: The namespace to add.
            position (int): The position to add the layer at. Defaults to 0.
            read_only (bool): Whether the layer is read-only. Defaults to False.
            priority (int): The priority of the layer. Defaults to 100.
        """
        self.layers.insert(position, (ns, read_only, priority))

    def get_layer(self, index: int):
        """
        Retrieves a specific layer by its index.

        Args:
            index (int): The index of the layer to retrieve.

        Returns:
            tuple: The namespace, read-only status, and priority of the layer.

        Raises:
            IndexError: If the index is out of bounds.
        """
        if index >= len(self.layers) or index < 0:
            raise IndexError(f"Layer index {index} out of bounds")
        return self.layers[index]

    def get_layer_by_name(self, name: str):
        """
        Retrieves a specific layer by its name.

        Args:
            name (str): The name of the layer to retrieve.

        Returns:
            tuple: The namespace, read-only status, and priority of the layer.

        Raises:
            ValueError: If the layer with the specified name is not found.
        """
        for ns, ro, p in self.layers:
            if ns.name == name:
                return ns, ro, p
        raise ValueError(f"Layer with name {name} not found")

    def set_layer_priority(self, ns, new_priority: int):
        """
        Sets the priority of a specific namespace layer.

        Args:
            ns: The namespace to set the priority for.
            new_priority (int): The new priority value.

        Raises:
            ValueError: If the namespace is not found in the layers.
        """
        for i, (n, ro, _) in enumerate(self.layers):
            if n == ns:
                self.layers[i] = (n, ro, new_priority)
                return
        raise ValueError("Namespace not found in layers")

    def update_layer(self, index: int, ns=None, read_only=None, priority=None):
        """
        Updates the attributes of a specific layer.

        Args:
            index (int): The index of the layer to update.
            ns: The new namespace to set (optional).
            read_only (bool): The new read-only status to set (optional).
            priority (int): The new priority to set (optional).

        Raises:
            IndexError: If the index is out of bounds.
        """
        if index >= len(self.layers) or index < 0:
            raise IndexError(f"Layer index {index} out of bounds")
        current_ns, current_ro, current_p = self.layers[index]
        self.layers[index] = (
            ns if ns is not None else current_ns,
            read_only if read_only is not None else current_ro,
            priority if priority is not None else current_p,
        )

    def remove_layer(self, ns):
        """
        Removes a namespace layer.

        Args:
            ns: The namespace to remove.
        """
        self.layers = [(n, ro, p) for (n, ro, p) in self.layers if n != ns]

    def list(self, path_prefix: str = ""):
        """
        Lists all paths with a specific prefix across all layers.

        Args:
            path_prefix (str): The prefix to filter paths. Defaults to "".

        Returns:
            list: All paths with the specified prefix.
        """
        seen = set()
        results = []
        for ns, _, _ in self._sorted_layers():
            for path in ns.list(path_prefix):
                if path not in seen:
                    seen.add(path)
                    results.append(path)
        return results

    def list_layers(self):
        """
        Lists all layers with their attributes.

        Returns:
            list: All layers with their attributes.
        """
        return [
            {"name": ns.name, "read_only": ro, "priority": p}
            for ns, ro, p in self._sorted_layers()
        ]

    def resolve_pattern(self, pattern: str):
        """
        Resolves a pattern across all layers.

        Args:
            pattern (str): The pattern to resolve.

        Returns:
            list: All matches for the pattern.
        """
        seen = set()
        matches = []
        for ns, _, _ in self._sorted_layers():
            for path, sym in ns.resolve_pattern(pattern):
                if path not in seen:
                    seen.add(path)
                    matches.append((path, sym))
        return matches

    def mount(self, mount_path: str, sub_namespace):
        """
        Mounts a sub-namespace under a specific prefix.

        Args:
            mount_path (str): The prefix to mount the sub-namespace under.
            sub_namespace: The sub-namespace to mount.

        Example:
            composite.mount("plugins.auth", plugin_ns)
        """

        class MountedNamespace:
            def __init__(self, base_path, delegate_ns):
                self.base_path = base_path
                self.ns = delegate_ns

            def resolve(self, path, **kwargs):
                if path.startswith(self.base_path):
                    subpath = path[len(self.base_path):].lstrip(".")
                    return self.ns.resolve(subpath)
                raise KeyError(f"{path} not in mounted prefix '{self.base_path}'")

            def resolve_pattern(self, pattern):
                if pattern.startswith(self.base_path):
                    subpattern = pattern[len(self.base_path):].lstrip(".")
                    matches = self.ns.resolve_pattern(subpattern)
                    return [(f"{self.base_path}.{p}", s) for p, s in matches]
                return []

            def list(self, path_prefix=""):
                if not path_prefix or path_prefix.startswith(self.base_path):
                    prefix = path_prefix[len(self.base_path):].lstrip(".")
                    return [f"{self.base_path}.{p}" for p in self.ns.list(prefix)]
                return []

            def register(self, path, value, **kwargs):
                if path.startswith(self.base_path):
                    subpath = path[len(self.base_path):].lstrip(".")
                    return self.ns.register(subpath, value, **kwargs)
                raise KeyError(f"{path} not in mounted prefix '{self.base_path}'")

        mounted = MountedNamespace(mount_path, sub_namespace)
        self.append_layer(mounted)

    def clear(self):
        """
        Clears all layers from the composite namespace.
        """
        self.layers.clear()

    def merge(self, other):
        """
        Merges another CompositeNamespace into the current one.

        Args:
            other (CompositeNamespace): The other CompositeNamespace to merge.

        Raises:
            TypeError: If the other object is not a CompositeNamespace.
        """
        if not isinstance(other, CompositeNamespace):
            raise TypeError("Can only merge with another CompositeNamespace")
        for ns, ro, p in other.layers:
            self.append_layer(ns, read_only=ro, priority=p)


def create_read_only_namespace(namespace) -> CompositeNamespace:
    """
    Creates a read-only namespace from an existing one.

    Args:
        namespace: The namespace to make read-only.

    Returns:
        CompositeNamespace: A composite namespace with the given namespace as read-only.
    """
    composite = CompositeNamespace()
    composite.append_layer(namespace, read_only=True)
    return composite

def merge_namespaces(*namespaces, name="merged"):
    """
    Merges multiple namespaces into a single CompositeNamespace.

    Args:
        *namespaces: The namespaces to merge.
        name (str): The name of the resulting composite namespace. Defaults to "merged".

    Returns:
        CompositeNamespace: The merged composite namespace.
    """
    composite = CompositeNamespace(name=name)
    for ns in namespaces:
        composite.append_layer(ns)
    return composite