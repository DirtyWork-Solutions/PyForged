from loguru import logger
from typing import Any, Callable, Tuple, Dict, List, cast

from forged.__bases__ import BaseNamespaceItem
from forged.elements.namespaces.core.items import Entry
from forged.elements.namespaces.core.nodes import NamespaceNode
from forged.elements.namespaces.utils import split_path

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
            existing_node.entry.value = new_value  # allow overwriting
        elif self.conflict_mode == "chain":
            if isinstance(existing_node.entry.value, list):
                existing_node.entry.value.append(new_value)
            elif callable(existing_node.entry.value) and callable(new_value):
                original_callable = existing_node.entry.value

                def chained_callable(*args, **kwargs):
                    original_callable(*args, **kwargs)
                    return new_value(*args, **kwargs)

                existing_node.entry.value = chained_callable
            else:
                existing_node.entry.value = [existing_node.entry.value, new_value]
        elif self.conflict_mode == "soft":
            # Do nothing, keep the existing value
            logger.info(f"Conflict at {path}: existing value retained in 'soft' mode.")
        elif self.conflict_mode == "strict":
            # Raise an exception
            raise ValueError(f"Conflict at {path}: symbol already exists in 'strict' mode.")


        else:
            raise ValueError(f"Unknown conflict mode: {self.conflict_mode}")

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

    def load_lazy(self, path: str) -> Entry:
        """
        Load a lazy item for a given path.
        """
        loader = self.lazy_registry.get(path)
        if not loader:
            logger.error(f"No lazy loader for path {path}")
            raise KeyError(f"No lazy loader for path {path}")
        return Entry(value=loader())

    def match_pattern(self, root: NamespaceNode, pattern: str) -> List[Tuple[str, BaseNamespaceItem]]:
            from forged.elements.namespaces.utils import split_path

            parts = split_path(pattern)
            results: List[Tuple[str, BaseNamespaceItem]] = []

            def dfs(node: NamespaceNode, path_so_far: List[str], remaining_parts: List[str]) -> None:
                if not remaining_parts:
                    if node.entry:
                        results.append((".".join(path_so_far), node.entry))
                    return

                current_part, *rest = remaining_parts
                logger.debug(f"DFS: So far={path_so_far}, Remaining={remaining_parts}")

                if current_part == "**":
                    # Recurse both with and without consuming the **
                    for child_name, child_node in node.children.items():
                        dfs(child_node, path_so_far + [child_name], remaining_parts)
                        dfs(child_node, path_so_far + [child_name], rest)
                elif current_part == "*":
                    for child_name, child_node in node.children.items():
                        dfs(child_node, path_so_far + [child_name], rest)
                else:
                    child_node = node.get_child(current_part)
                    logger.debug(
                        f"DFS: node.get_child('{current_part}') -> {child_node}, id={id(child_node) if child_node else 'N/A'}")
                    if child_node is not None:
                        dfs(child_node, path_so_far + [current_part], rest)
                    else:
                        logger.debug(f"No child named '{current_part}' found under node '{node.name}'")

                logger.debug(f"DFS: node id={id(node)}, node.name={node.name}")
                logger.debug(f"DFS: node.children keys: {list(node.children.keys())}")

            # First attempt from given root
            dfs(root, [], parts)

            # Optional fallback: if no match and root has a name, try using it as prefix
            if not results and root.name:
                logger.debug(f"No match found; retrying with root prefix: {root.name}")
                dfs(root, [root.name], parts)

            return results

    def resolve_with_context(self, entries: list[Entry], context: dict) -> Entry:
        """
        Pick the best matching entry based on metadata/context.
        """
        # First: exact match on all keys
        for entry in entries:
            if all(entry.metadata.get(k) == v for k, v in context.items()):
                return entry

        # Second: partial match (at least one key)
        for entry in entries:
            if any(entry.metadata.get(k) == v for k, v in context.items()):
                return entry

        # Fallback: return first
        return entries[0]