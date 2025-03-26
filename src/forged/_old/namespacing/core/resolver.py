from loguru import logger
from typing import Any, Optional, Callable, List, Tuple, Dict

from src.forged._old.namespacing import Symbol
from src.forged._old.namespacing import NamespaceNode
from src.forged._old.namespacing import split_path

_conflict_modes = [
    'soft',
    'strict',
    'chain',
    'replace'
]

class Resolver:
    def __init__(self):
        self.conflict_mode: str = "strict"
        self.lazy_registry: Dict[str, Callable] = {}

    def handle_conflict(self, existing_node: NamespaceNode, new_value: Any, path: str) -> None:
        """
        Handle conflicts based on the conflict mode.
        """
        if self.conflict_mode == "replace":
            return  # allow overwrite
        elif self.conflict_mode == "chain":
            if isinstance(existing_node.symbol.value, list):
                existing_node.symbol.value.append(new_value)
            elif callable(existing_node.symbol.value) and callable(new_value):
                original_callable = existing_node.symbol.value

                def chained_callable(*args, **kwargs):
                    original_callable(*args, **kwargs)
                    new_value(*args, **kwargs)

                existing_node.symbol.value = chained_callable
            else:
                existing_node.symbol.value = [existing_node.symbol.value, new_value]
        else:
            raise ValueError(f"Conflict at {path}: symbol already exists.")

    def bind_lazy(self, path: str, loader: Callable) -> None:
        """
        Bind a lazy loader to a path.
        """
        self.lazy_registry[path] = loader

    def has_lazy(self, path: str) -> bool:
        """
        Check if a lazy loader is bound to a path.
        """
        return path in self.lazy_registry

    def load_lazy(self, path: str) -> Symbol:
        """
        Load a lazy symbol for a given path.
        """
        loader = self.lazy_registry.get(path)
        if not loader:
            logger.error(f"No lazy loader for path {path}")
            raise KeyError(f"No lazy loader for path {path}")
        return Symbol(value=loader())

    def match_pattern(
            self,
            root: NamespaceNode,
            pattern: str
    ) -> List[Tuple[str, Symbol]]:
        """
        Match a pattern against the namespace tree.
        """
        parts = split_path(pattern)
        results: List[Tuple[str, Symbol]] = []

        def dfs(node: NamespaceNode, path_so_far: List[str], remaining_parts: List[str]) -> None:
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