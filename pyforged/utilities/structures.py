from collections import deque


# 6.1 Bidirectional Dictionary
class BiDict:
    """A dictionary where values can be used as keys."""
    def __init__(self):
        self.forward = {}
        self.backward = {}

    def add(self, key, value):
        self.forward[key] = value
        self.backward[value] = key

    def get_by_key(self, key):
        return self.forward.get(key)

    def get_by_value(self, value):
        return self.backward.get(value)

# 6.5 Circular Buffer
class CircularBuffer:
    """Fixed-size queue with automatic removal of old elements."""
    def __init__(self, size: int):
        self.buffer = deque(maxlen=size)

    def add(self, item):
        self.buffer.append(item)

    def get_all(self):
        return list(self.buffer)