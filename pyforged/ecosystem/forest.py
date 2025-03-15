import dataclasses
import os
import socket
import threading
from typing import Any, Dict

from pyforged.utilities.misc import is_package_installed


class PyForgedEcosystem:
    """A singleton-based manager for storing and retrieving application metadata."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(PyForgedEcosystem, cls).__new__(cls)
                cls._instance._metadata = {
                    "app_name": "My Application",
                    "version": "1.0.0",
                    "author": "Your Name",
                    "description": "Default Application Description",
                    "environment": os.getenv("APP_ENV", "development"),
                    "hostname": socket.gethostname(),
                    "execution_id": os.urandom(8).hex(),
                    "project_flags": {
                        "bedrocked": True if is_package_installed("bedrocked") else False,
                        "runecaller": True,
                        "essencebinder": False,
                        "hexcrafter": False,
                        "concordance": False,
                        "gaugework": False,
                        "covenantledger": False,
                        "ironpath": False
                    }
                }
            return cls._instance

    def set(self, key: str, value: Any) -> None:
        """Store a metadata value."""
        self._metadata[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a metadata value."""
        return self._metadata.get(key, default)

    def add_project(self, key: str, value: bool = False) -> None:
        """Add a """
        self._metadata["project_flags"][key] = value

    def enable_project(self, feature: str, create_missing: bool = False) -> None:
        """Enable a feature flag."""
        if feature not in self._metadata.keys() and not create_missing:
            raise KeyError(f"'{feature}' does not exist as a flag.")
        else:
            self._metadata["project_flags"][feature] = True

    def disable_project(self, feature: str) -> None:
        """Disable a feature flag."""
        self._metadata["project_flags"][feature] = False

    def is_project_enabled(self, feature: str) -> bool:
        """Check if a feature flag is enabled."""
        return self._metadata["project_flags"].get(feature, False)


# Example usage
if __name__ == "__main__":
    meta = PyForgedEcosystem()
    print("App Name:", meta.get("app_name"))
    print("Environment:", meta.get("environment"))


    meta.enable_project("dark_mode", True)
    print("Is Dark Mode Enabled?", meta.is_project_enabled("cryptography"))
    print("Is Dark Mode Installed?", is_package_installed("keyring"))
