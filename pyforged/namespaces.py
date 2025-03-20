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
import re
import time
import collections

class NamespaceManager:
    """A thread-safe manager for handling namespaced items in a hierarchical structure."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(NamespaceManager, cls).__new__(cls)
                cls._instance._namespaces = {}
                cls._instance._metadata = {}
                cls._instance._aliases = {}
                cls._instance._versions = collections.defaultdict(list)
                cls._instance._permissions = {}
                cls._instance._expirations = {}
                cls._instance._namespace_lock = threading.RLock()
            return cls._instance

    def _validate_namespace(self, namespace: str) -> bool:
        """Validate the namespace key format.

        Args:
            namespace (str): The hierarchical key to validate.

        Returns:
            bool: True if the namespace is valid, False otherwise.
        """
        pattern = r'^[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*$'
        return bool(re.match(pattern, namespace))

    def _resolve_alias(self, namespace: str) -> str:
        """Resolve the namespace alias to its actual namespace.

        Args:
            namespace (str): The namespace or alias to resolve.

        Returns:
            str: The resolved namespace.
        """
        return self._aliases.get(namespace, namespace)

    def set_alias(self, alias: str, namespace: str) -> None:
        """Set an alias for a namespace.

        Args:
            alias (str): The alias to set.
            namespace (str): The actual namespace.
        """
        if not self._validate_namespace(alias) or not self._validate_namespace(namespace):
            raise ValueError("Invalid alias or namespace format.")
        with self._namespace_lock:
            self._aliases[alias] = namespace

    def get_alias(self, alias: str) -> Union[str, None]:
        """Get the actual namespace for an alias.

        Args:
            alias (str): The alias to resolve.

        Returns:
            Union[str, None]: The actual namespace or None if alias does not exist.
        """
        with self._namespace_lock:
            return self._aliases.get(alias)

    def delete_alias(self, alias: str) -> None:
        """Delete an alias.

        Args:
            alias (str): The alias to delete.
        """
        with self._namespace_lock:
            self._aliases.pop(alias, None)

    def set_permission(self, namespace: str, role: str, permission: str) -> None:
        """Set a permission for a namespace.

        Args:
            namespace (str): The hierarchical key.
            role (str): The role to set the permission for.
            permission (str): The permission to set (e.g., 'read', 'write').
        """
        if not self._validate_namespace(namespace):
            raise ValueError(f"Invalid namespace format: {namespace}")
        with self._namespace_lock:
            self._permissions.setdefault(namespace, {}).setdefault(role, set()).add(permission)

    def get_permissions(self, namespace: str) -> Dict[str, List[str]]:
        """Get all permissions for a namespace.

        Args:
            namespace (str): The hierarchical key.

        Returns:
            Dict[str, List[str]]: A dictionary of roles and their permissions.
        """
        namespace = self._resolve_alias(namespace)
        with self._namespace_lock:
            return {role: list(perms) for role, perms in self._permissions.get(namespace, {}).items()}

    def check_permission(self, namespace: str, role: str, permission: str) -> bool:
        """Check if a role has a specific permission for a namespace.

        Args:
            namespace (str): The hierarchical key.
            role (str): The role to check.
            permission (str): The permission to check.

        Returns:
            bool: True if the role has the permission, False otherwise.
        """
        namespace = self._resolve_alias(namespace)
        with self._namespace_lock:
            return permission in self._permissions.get(namespace, {}).get(role, set())

    def set(self, namespace: str, value: Any, description: str = "", role: str = "admin", ttl: int = None) -> None:
        """Store a value under a structured namespace with metadata, versioning, and optional expiration.

        Args:
            namespace (str): The hierarchical key (e.g., 'services.cache.config').
            value (Any): The value to store.
            description (str, optional): A description of the namespace.
            role (str, optional): The role performing the operation.
            ttl (int, optional): Time-to-live in seconds for the namespace.
        """
        namespace = self._resolve_alias(namespace)
        if not self._validate_namespace(namespace):
            raise ValueError(f"Invalid namespace format: {namespace}")
        if not self.check_permission(namespace, role, "write"):
            raise PermissionError(f"Role '{role}' does not have write permission for namespace '{namespace}'")

        with self._namespace_lock:
            keys = namespace.split(".")
            ref = self._namespaces
            for key in keys[:-1]:
                ref = ref.setdefault(key, {})
            ref[keys[-1]] = value

            # Store metadata
            self._metadata[namespace] = {
                "created_at": time.time(),
                "updated_at": time.time(),
                "description": description
            }

            # Store version
            self._versions[namespace].append((time.time(), value))

            # Set expiration if ttl is provided
            if ttl is not None:
                self._expirations[namespace] = time.time() + ttl

    def get(self, namespace: str, default: Any = None, role: str = "admin") -> Any:
        """Retrieve a value from a structured namespace.

        Args:
            namespace (str): The hierarchical key.
            default (Any, optional): The default value if the key is not found.
            role (str, optional): The role performing the operation.

        Returns:
            Any: The stored value or the default.
        """
        namespace = self._resolve_alias(namespace)
        if not self.check_permission(namespace, role, "read"):
            raise PermissionError(f"Role '{role}' does not have read permission for namespace '{namespace}'")

        with self._namespace_lock:
            # Check for expiration
            if namespace in self._expirations and time.time() > self._expirations[namespace]:
                self.delete(namespace, role)
                return default

            keys = namespace.split(".")
            ref = self._namespaces
            for key in keys:
                if key not in ref:
                    return default
                ref = ref[key]
            return ref

    def get_metadata(self, namespace: str) -> Dict[str, Any]:
        """Retrieve metadata for a namespace.

        Args:
            namespace (str): The hierarchical key.

        Returns:
            Dict[str, Any]: The metadata dictionary.
        """
        namespace = self._resolve_alias(namespace)
        with self._namespace_lock:
            return self._metadata.get(namespace, {})

    def get_versions(self, namespace: str) -> List[Dict[str, Any]]:
        """Retrieve all versions of a namespace.

        Args:
            namespace (str): The hierarchical key.

        Returns:
            List[Dict[str, Any]]: A list of versions with timestamps.
        """
        namespace = self._resolve_alias(namespace)
        with self._namespace_lock:
            return [{"timestamp": ts, "value": val} for ts, val in self._versions.get(namespace, [])]

    def rollback(self, namespace: str, timestamp: float) -> None:
        """Rollback a namespace to a specific version.

        Args:
            namespace (str): The hierarchical key.
            timestamp (float): The timestamp to rollback to.
        """
        namespace = self._resolve_alias(namespace)
        with self._namespace_lock:
            versions = self._versions.get(namespace, [])
            for ts, val in reversed(versions):
                if ts <= timestamp:
                    self.set(namespace, val)
                    break

    def delete(self, namespace: str, role: str = "admin") -> None:
        """Remove a value from the structured namespace and its metadata.

        Args:
            namespace (str): The hierarchical key.
            role (str, optional): The role performing the operation.
        """
        namespace = self._resolve_alias(namespace)
        if not self.check_permission(namespace, role, "write"):
            raise PermissionError(f"Role '{role}' does not have write permission for namespace '{namespace}'")

        with self._namespace_lock:
            keys = namespace.split(".")
            ref = self._namespaces
            for key in keys[:-1]:
                if key not in ref:
                    return
                ref = ref[key]
            ref.pop(keys[-1], None)
            self._metadata.pop(namespace, None)
            self._versions.pop(namespace, None)
            self._expirations.pop(namespace, None)

    def list_keys(self, namespace: str = "") -> List[str]:
        """List all keys under a given namespace.

        Args:
            namespace (str, optional): The namespace to list keys from.

        Returns:
            List[str]: A list of namespaced keys.
        """
        namespace = self._resolve_alias(namespace)
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
    ns_manager.set_permission("services.database.connection", "admin", "read")
    ns_manager.set_permission("services.database.connection", "admin", "write")
    ns_manager.set("services.database.connection", "postgres://user:pass@localhost/db", "Database connection string", role="admin", ttl=10)
    print(ns_manager.get("services.database.connection", role="admin"))  # Should print the database connection string
    time.sleep(11)
    print(ns_manager.get("services.database.connection", role="admin"))  # Should print None as the value has expiredget("services.database.connection", role="admin"))  # Should print None