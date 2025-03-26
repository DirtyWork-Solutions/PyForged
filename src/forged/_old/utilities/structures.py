from collections import deque


# 6.1 Bidirectional Dictionary
class BiDict:
    """A dictionary where values can be used as keys."""
    def __init__(self):
        self.forward = {}
        self.backward = {}

    def add(self, key, value):
        if key in self.forward or value in self.backward:
            raise ValueError("Duplicate key or value not allowed.")
        self.forward[key] = value
        self.backward[value] = key

    def remove_by_key(self, key):
        value = self.forward.pop(key, None)
        if value:
            del self.backward[value]

    def remove_by_value(self, value):
        key = self.backward.pop(value, None)
        if key:
            del self.forward[key]

    def get_by_key(self, key):
        return self.forward.get(key)

    def get_by_value(self, value):
        return self.backward.get(value)

    def __len__(self):
        return len(self.forward)

    def __contains__(self, key):
        return key in self.forward

# 6.5 Circular Buffer
class CircularBuffer:
    """Fixed-size queue with automatic removal of old elements."""
    def __init__(self, size: int):
        self.buffer = deque(maxlen=size)
        self.size = size

    def add(self, item):
        """Add an item to the buffer."""
        self.buffer.append(item)

    def get_all(self):
        """Retrieve all items from the buffer."""
        return list(self.buffer)

    def is_full(self):
        """Check if the buffer is full."""
        return len(self.buffer) == self.size

    def is_empty(self):
        """Check if the buffer is empty."""
        return len(self.buffer) == 0

    def clear(self):
        """Clear all items from the buffer."""
        self.buffer.clear()


import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, item, priority):
        heapq.heappush(self.heap, (priority, item))

    def pop(self):
        return heapq.heappop(self.heap)[1]

    def is_empty(self):
        return len(self.heap) == 0


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True