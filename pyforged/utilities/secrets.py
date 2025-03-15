"""
Secrets Manager Module

This module provides a secure and thread-safe way to store, retrieve, and manage secrets.
Secrets are encrypted in memory using AES-based Fernet encryption and can be stored with
optional expiration times (TTL). Additionally, secrets can be loaded from environment variables
and exported/imported securely.

Features:
- Singleton pattern to ensure a single instance of SecretsManager.
- In-memory encryption for stored secrets.
- TTL-based expiration for temporary secrets.
- Environment variable loading (SECRETS_ prefix).
- Secure import/export of secrets to encrypted files.

Dependencies:
- `cryptography` for secure encryption.

Usage:
```python
secrets_manager = SecretsManager()
secrets_manager.set_secret("api_key", "super_secret_value", ttl=60)
print(secrets_manager.get_secret("api_key"))
```
"""

import threading
import os
import base64
import json
from cryptography.fernet import Fernet

class SecretsManager:
    """A singleton-based secrets manager for secure storage and retrieval."""
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(SecretsManager, cls).__new__(cls)
                cls._instance._secrets = {}
                cls._instance._secrets_lock = threading.RLock()
                cls._instance._load_from_env()
                cls._instance._encryption_key = cls._generate_key()
                cls._instance._cipher = Fernet(cls._instance._encryption_key)
            return cls._instance

    @staticmethod
    def _generate_key():
        """Generate or retrieve an encryption key from the environment."""
        key = os.environ.get("SECRETS_MANAGER_KEY")
        if not key:
            key = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")
            os.environ["SECRETS_MANAGER_KEY"] = key
        return key.encode("utf-8")

    def _encrypt(self, data):
        """Encrypt a secret before storing it."""
        return self._cipher.encrypt(json.dumps(data).encode()).decode()

    def _decrypt(self, encrypted_data):
        """Decrypt a secret before retrieval."""
        return json.loads(self._cipher.decrypt(encrypted_data.encode()).decode())

    def _load_from_env(self):
        """Load secrets from environment variables with the SECRETS_ prefix."""
        for key, value in os.environ.items():
            if key.startswith("SECRETS_"):
                self._secrets[key[8:]] = value

    def set_secret(self, key, secret, ttl=None):
        """Store an encrypted secret with an optional TTL (time-to-live).

        Args:
            key (str): The identifier for the secret.
            secret (any): The secret value to store.
            ttl (int, optional): The number of seconds before the secret is deleted.
        """
        with self._secrets_lock:
            encrypted_secret = {"data": self._encrypt(secret), "expires": None}
            if ttl:
                encrypted_secret["expires"] = threading.Timer(ttl, lambda: self.delete_secret(key))
                encrypted_secret["expires"].start()
            self._secrets[key] = encrypted_secret

    def get_secret(self, key, default=None):
        """Retrieve and decrypt a secret, returning a default if not found.

        Args:
            key (str): The identifier for the secret.
            default (any, optional): The default value to return if the secret is missing.

        Returns:
            any: The decrypted secret value or the default.
        """
        with self._secrets_lock:
            secret_data = self._secrets.get(key)
            if not secret_data:
                return default
            return self._decrypt(secret_data["data"])

    def delete_secret(self, key):
        """Remove a secret from the store.

        Args:
            key (str): The identifier of the secret to delete.
        """
        with self._secrets_lock:
            if key in self._secrets and self._secrets[key]["expires"]:
                self._secrets[key]["expires"].cancel()
            self._secrets.pop(key, None)

    def list_secrets(self):
        """List all stored secret keys without revealing values.

        Returns:
            list: A list of stored secret keys.
        """
        with self._secrets_lock:
            return list(self._secrets.keys())

    def export_secrets(self, filepath):
        """Export all secrets to an encrypted file.

        Args:
            filepath (str): The file path where secrets should be exported.
        """
        with self._secrets_lock:
            with open(filepath, "wb") as file:
                file.write(self._cipher.encrypt(json.dumps(self._secrets).encode()))

    def import_secrets(self, filepath):
        """Import secrets from an encrypted file.

        Args:
            filepath (str): The file path from where secrets should be imported.
        """
        with self._secrets_lock:
            with open(filepath, "rb") as file:
                self._secrets = json.loads(self._cipher.decrypt(file.read()).decode())

# Example usage:
if __name__ == "__main__":
    secrets_manager = SecretsManager()
    secrets_manager.set_secret("api_key", {"user": "supersecretvalue", "pass": "password"}, ttl=60)
    print("API Key:", secrets_manager.get_secret("api_key"))
    secrets_manager.export_secrets("secrets.enc")
    secrets_manager.import_secrets("secrets.enc")