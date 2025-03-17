"""
This module provides a centralized way to manage namespaced keys and hierarchical structures
for various components such as services, secrets, events, and other stored entities.

**Features:**
    - Create and manage hierarchical namespaces.
    - Retrieve items based on fully qualified names.
    - List and organize items under structured namespaces.
    - Support for wildcard-based retrieval.
    - Thread-safe operations.


**Usage:**

    namespace_manager = NamespaceManager()
    namespace_manager.set("secrets.api.key", "super_secret_value")
    print(namespace_manager.get("secrets.api.key"))

"""

import threading
from typing import Any, Dict, List, Union

class NamespaceManager:
    """A thread-safe manager for handling namespaced items in a hierarchical structure."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(NamespaceManager, cls).__new__(cls)
                cls._instance._namespaces = {}
                cls._instance._namespace_lock = threading.RLock()
            return cls._instance

    def set(self, namespace: str, value: Any) -> None:
        """Store a value under a structured namespace.

        Args:
            namespace (str): The hierarchical key (e.g., 'services.cache.config').
            value (Any): The value to store.
        """
        with self._namespace_lock:
            keys = namespace.split(".")
            ref = self._namespaces
            for key in keys[:-1]:
                ref = ref.setdefault(key, {})
            ref[keys[-1]] = value

    def get(self, namespace: str, default: Any = None) -> Any:
        """Retrieve a value from a structured namespace.

        Args:
            namespace (str): The hierarchical key.
            default (Any, optional): The default value if the key is not found.

        Returns:
            Any: The stored value or the default.
        """
        with self._namespace_lock:
            keys = namespace.split(".")
            ref = self._namespaces
            for key in keys:
                if key not in ref:
                    return default
                ref = ref[key]
            return ref

    def delete(self, namespace: str) -> None:
        """Remove a value from the structured namespace.

        Args:
            namespace (str): The hierarchical key.
        """
        with self._namespace_lock:
            keys = namespace.split(".")
            ref = self._namespaces
            for key in keys[:-1]:
                if key not in ref:
                    return
                ref = ref[key]
            ref.pop(keys[-1], None)

    def list_keys(self, namespace: str = "") -> List[str]:
        """List all keys under a given namespace.

        Args:
            namespace (str, optional): The namespace to list keys from.

        Returns:
            List[str]: A list of namespaced keys.
        """
        with self._namespace_lock:
            ref = self._namespaces
            if namespace:
                keys = namespace.split(".")
                for key in keys:
                    if key not in ref:
                        return []
                    ref = ref[key]
            return list(ref.keys())

    def search(self, pattern: str) -> Dict[str, Any]:
        """Retrieve all keys matching a namespace pattern with wildcards.

        Args:
            pattern (str): The wildcard pattern (e.g., 'services.*.config').

        Returns:
            Dict[str, Any]: Matching namespace-value pairs.
        """
        def match_keys(namespace_dict, path, collected):
            for key, value in namespace_dict.items():
                new_path = f"{path}.{key}" if path else key
                if isinstance(value, dict):
                    match_keys(value, new_path, collected)
                else:
                    collected[new_path] = value

        collected_matches = {}
        with self._namespace_lock:
            match_keys(self._namespaces, "", collected_matches)
        return {k: v for k, v in collected_matches.items() if self._match_pattern(k, pattern)}

    def _match_pattern(self, key: str, pattern: str) -> bool:
        """Helper function to check if a key matches a wildcard pattern."""
        from fnmatch import fnmatch
        return fnmatch(key, pattern)

# Example usage
if __name__ == "__main__":
    ns_manager = NamespaceManager()
    ns_manager.set("services.database.connection", "postgres://user:pass@localhost/db")
    ns_manager.set("services.cache.config", {"timeout": 30, "backend": "redis"})
    print(ns_manager.get("services.database.connection"))
    ns_manager.delete("services.database.connection")
    print(ns_manager.list_keys("services"))
    print(ns_manager.search("services.*.config"))
