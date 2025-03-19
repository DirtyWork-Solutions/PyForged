class DotDict(dict):
    """
    A dictionary subclass that allows access to keys via dot notation.
    """
    def __getattr__(self, item: str):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{item}'")

    def __setattr__(self, key: str, value):
        self[key] = value

    def __delattr__(self, item: str):
        try:
            del self[item]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{item}'")

    def to_dict(self) -> dict:
        """
        Converts the DotDict back to a regular dictionary.
        """
        return dict(self)

    def update_from_dict(self, other_dict: dict):
        """
        Updates the DotDict with key-value pairs from another dictionary.
        """
        for key, value in other_dict.items():
            self[key] = value

    def get_nested(self, dot_key: str):
        """
        Retrieves a value from a nested dictionary using a dot-separated key.
        """
        keys = dot_key.split('.')
        value = self
        for key in keys:
            value = value[key]
        return value

    def __repr__(self) -> str:
        return f"DotDict({super().__repr__()})"

    def __contains__(self, key: str) -> bool:
        return key in self

    def __iter__(self):
        return iter(self.keys())

    def __len__(self) -> int:
        return len(self)

    def __getitem__(self, key: str):
        return super().__getitem__(key)

    def __setitem__(self, key: str, value):
        super().__setitem__(key, value)

class MetadataDict(DotDict):
    """
    A dictionary subclass that allows access to keys via dot notation,
    specifically designed for metadata handling.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Additional initialization if needed

    def merge(self, other_dict):
        """
        Merges another dictionary into the MetadataDict.
        """
        for key, value in other_dict.items():
            self[key] = value

    def filter_keys(self, keys):
        """
        Returns a new MetadataDict containing only the specified keys.
        """
        return MetadataDict({key: self[key] for key in keys if key in self})

    def to_json(self):
        """
        Converts the MetadataDict to a JSON string.
        """
        import json
        return json.dumps(self)

    @property
    def keys_list(self):
        """
        Returns a list of all keys in the MetadataDict.
        """
        return list(self.keys())

    @property
    def values_list(self):
        """
        Returns a list of all values in the MetadataDict.
        """
        return list(self.values())

    def remove_keys(self, keys):
        """
        Removes the specified keys from the MetadataDict.
        """
        for key in keys:
            if key in self:
                del self[key]

    def key_exists(self, key):
        """
        Checks if a key exists in the MetadataDict.
        """
        return key in self

    def get_with_default(self, key, default=None):
        """
        Returns the value for a key, or a default value if the key does not exist.
        """
        return self.get(key, default)

    def clear_all(self):

        """
        Clears all keys from the MetadataDict.
        """
        self.clear()

    def update_values(self, other_dict):
        """
        Updates the values of existing keys from another dictionary.
        """
        for key, value in other_dict.items():
            if key in self:
                self[key] = value

    def rename_key(self, old_key, new_key):
        """
        Renames a key in the MetadataDict.
        """
        if old_key in self:
            self[new_key] = self.pop(old_key)

    def keys_with_prefix(self, prefix):
        """
        Returns a list of keys that start with the given prefix.
        """
        return [key for key in self.keys() if key.startswith(prefix)]