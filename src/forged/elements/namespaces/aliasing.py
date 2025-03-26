from typing import Dict

class Aliaser:
    def __init__(self):
        self._aliases: Dict[str, str] = {}

    def add(self, alias: str, target: str):
        self._aliases[alias] = target

    def remove(self, alias: str):
        self._aliases.pop(alias, None)

    def get(self, path: str) -> str:
        return self._aliases.get(path, path)

    def resolve_path(self, path: str) -> str:
        """
        Supports partial alias resolution by replacing matching prefix segments.
        """
        matched_alias = None
        for alias_prefix in sorted(self._aliases.keys(), key=lambda x: -len(x)):
            if path == alias_prefix or path.startswith(alias_prefix + "."):
                matched_alias = alias_prefix
                break

        if matched_alias:
            suffix = path[len(matched_alias):].lstrip(".")
            real_path = self._aliases[matched_alias]
            return f"{real_path}.{suffix}" if suffix else real_path

        return path

    def all(self) -> Dict[str, str]:
        return self._aliases.copy()

if __name__ == '__main__':
    from forged.elements.namespaces.core.namespace import Namespace

    ns = Namespace("models")

    ns.register("models.v2.prod.infer", lambda: "new")
    ns.add_alias("model.latest", "models.v2.prod")

    print(ns.resolve("model.latest.infer")())  # Should print: "new"
