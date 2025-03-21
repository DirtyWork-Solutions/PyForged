from typing import Any, Optional, Callable, List, Tuple

from forged.namespacing import Symbol
from forged.namespacing.core.node import NamespaceNode
from forged.namespacing.core.utils import split_path


class Resolver:
    def __init__(self):
        self.conflict_mode = "strict"
        self.lazy_registry = {}

    def handle_conflict(self, existing_node, new_value, path):
        if self.conflict_mode == "replace":
            return  # allow overwrite
        elif self.conflict_mode == "chain":
            # TODO: chain values (e.g. append to list or callable chain)
            pass
        else:
            raise ValueError(f"Conflict at {path}: symbol already exists.")

    def bind_lazy(self, path: str, loader: Callable):
        self.lazy_registry[path] = loader

    def has_lazy(self, path: str) -> bool:
        return path in self.lazy_registry

    def load_lazy(self, path: str):
        loader = self.lazy_registry.get(path)
        if not loader:
            raise KeyError(f"No lazy loader for path {path}")
        return Symbol(value=loader())  # or wrap in Symbol if needed

    def match_pattern(
            self,
            root: NamespaceNode,
            pattern: str
    ) -> List[Tuple[str, 'Symbol']]:
        parts = split_path(pattern)
        results = []

        def dfs(node, path_so_far, remaining_parts):
            if not remaining_parts:
                if node.symbol:
                    results.append((".".join(path_so_far), node.symbol))
                return

            current = remaining_parts[0]
            rest = remaining_parts[1:]

            if current == "**":
                # Match this level and recurse deeply
                if node.symbol:
                    results.append((".".join(path_so_far), node.symbol))
                for child_name, child_node in node.children.items():
                    # ** matches 0 or more, so continue with both:
                    dfs(child_node, path_so_far + [child_name], remaining_parts)  # keep **
                    dfs(child_node, path_so_far + [child_name], rest)  # move on
            elif current == "*":
                for child_name, child_node in node.children.items():
                    dfs(child_node, path_so_far + [child_name], rest)
            else:
                child_node = node.get_child(current)
                if child_node:
                    dfs(child_node, path_so_far + [current], rest)

        dfs(root, [], parts)
        return results