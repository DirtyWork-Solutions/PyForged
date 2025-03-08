# secrets.py

import threading

class SecretsManager:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(SecretsManager, cls).__new__(cls)
                cls._instance._secrets = {}
                cls._instance._secrets_lock = threading.RLock()
            return cls._instance

    def set_secret(self, key, secret):
        """Store a secret associated with a key."""
        with self._secrets_lock:
            self._secrets[key] = secret

    def get_secret(self, key, default=None):
        """Retrieve a secret; returns default if key is not found."""
        with self._secrets_lock:
            return self._secrets.get(key, default)

    def delete_secret(self, key):
        """Remove a secret from the store."""
        with self._secrets_lock:
            self._secrets.pop(key, None)

# Example usage:
if __name__ == "__main__":
    secrets_manager = SecretsManager()
    secrets_manager.set_secret("api_key", "supersecretvalue")
    print("API Key:", secrets_manager.get_secret("api_key"))
