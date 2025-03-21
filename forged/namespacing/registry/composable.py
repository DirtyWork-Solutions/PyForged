class CompositeNamespace:
    def __init__(self, *namespaces, name="composite"):
        self.name = name
        self.layers = []  # list of (namespace, read_only, priority)
        for ns in namespaces:
            self.append_layer(ns)

    def _sorted_layers(self):
        return sorted(self.layers, key=lambda item: item[2], reverse=True)

    def resolve(self, path: str, **kwargs):
        for ns, _, _ in self._sorted_layers():
            try:
                return ns.resolve(path, **kwargs)
            except KeyError:
                continue
        raise KeyError(f"Path not found in composite: {path}")

    def resolve_all(self, path: str):
        results = []
        for ns, _, _ in self._sorted_layers():
            try:
                results.append(ns.resolve(path))
            except KeyError:
                continue
        return results

    def register(self, path: str, value, layer: int = 0, **kwargs):
        if layer >= len(self.layers):
            raise IndexError(f"Layer index {layer} out of bounds")
        ns, read_only, _ = self.layers[layer]
        if read_only:
            raise PermissionError(f"Cannot register in read-only layer: {ns.name}")
        ns.register(path, value, **kwargs)

    def append_layer(self, ns, read_only=False, priority=100):
        self.layers.append((ns, read_only, priority))

    def add_layer(self, ns, position=0, read_only=False, priority=100):
        self.layers.insert(position, (ns, read_only, priority))

    def set_layer_priority(self, ns, new_priority: int):
        for i, (n, ro, _) in enumerate(self.layers):
            if n == ns:
                self.layers[i] = (n, ro, new_priority)
                return
        raise ValueError("Namespace not found in layers")

    def remove_layer(self, ns):
        self.layers = [(n, ro, p) for (n, ro, p) in self.layers if n != ns]

    def list(self, path_prefix: str = ""):
        seen = set()
        results = []
        for ns, _, _ in self._sorted_layers():
            for path in ns.list(path_prefix):
                if path not in seen:
                    seen.add(path)
                    results.append(path)
        return results

    def list_layers(self):
        return [
            {"name": ns.name, "read_only": ro, "priority": p}
            for ns, ro, p in self._sorted_layers()
        ]

    def resolve_pattern(self, pattern: str):
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
        Mount a namespace under a specific prefix.
        Example: composite.mount("plugins.auth", plugin_ns)
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