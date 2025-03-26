# state.py

import threading

class SharedState:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(SharedState, cls).__new__(cls)
                cls._instance._state = {}
                cls._instance._state_lock = threading.RLock()
            return cls._instance

    def get(self, key, default=None):
        with self._state_lock:
            return self._state.get(key, default)

    def set(self, key, value):
        with self._state_lock:
            self._state[key] = value

    def delete(self, key):
        with self._state_lock:
            self._state.pop(key, None)

    def update(self, **kwargs):
        with self._state_lock:
            self._state.update(kwargs)

    def clear(self):
        with self._state_lock:
            self._state.clear()

    def keys(self):
        with self._state_lock:
            return list(self._state.keys())

    def items(self):
        with self._state_lock:
            return list(self._state.items())

# Example usage:
if __name__ == "__main__":
    state = SharedState()
    state.set("user_count", 10)
    print("User count:", state.get("user_count"))
