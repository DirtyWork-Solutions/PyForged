"""
Common and generic but productive class mix-ins.

This module provides a set of mix-ins for common functionalities such as serialization to JSON and YAML,
singleton pattern implementation, observer pattern implementation, and a custom `__repr__` method.
"""

import json
import yaml


class JSONSerializedBasic:
    """
    A mix-in class to provide JSON serialization and deserialization methods.
    """

    def to_json(self):
        """
        Serialize the instance to a JSON string.

        :return: JSON string representation of the instance.
        """
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        """
        Deserialize a JSON string to an instance of the class.

        :param json_str: JSON string to deserialize.
        :return: An instance of the class with attributes set from the JSON string.
        """
        data = json.loads(json_str)
        instance = cls()
        instance.__dict__.update(data)
        return instance


class YAMLSerializedBasic:
    """
    A mix-in class to provide YAML serialization and deserialization methods.
    """

    def to_yaml(self):
        """
        Serialize the instance to a YAML string.

        :return: YAML string representation of the instance.
        """
        return yaml.dump(self.__dict__)

    @classmethod
    def from_yaml(cls, yaml_str):
        """
        Deserialize a YAML string to an instance of the class.

        :param yaml_str: YAML string to deserialize.
        :return: An instance of the class with attributes set from the YAML string.
        """
        data = yaml.safe_load(yaml_str)
        instance = cls()
        instance.__dict__.update(data)
        return instance


class SerializedMixin(JSONSerializedBasic, YAMLSerializedBasic):
    """
    A mix-in class that combines JSON and YAML serialization and deserialization methods.
    """

    def serialize_to_file(self, file_path, format='json'):
        """
        Serialize the instance to a file in the specified format.

        :param file_path: Path to the file where the instance will be serialized.
        :param format: Format of the serialization ('json' or 'yaml').
        :raise ValueError: If the format is not supported.
        """
        with open(file_path, 'w') as file:
            if format == 'json':
                file.write(self.to_json())
            elif format == 'yaml':
                file.write(self.to_yaml())
            else:
                raise ValueError("Unsupported format. Use 'json' or 'yaml'.")

    @classmethod
    def deserialize_from_file(cls, file_path, format='json'):
        """
        Deserialize an instance from a file in the specified format.

        :param file_path: Path to the file from which the instance will be deserialized.
        :param format: Format of the serialization ('json' or 'yaml').
        :return: An instance of the class with attributes set from the file content.
        :raise ValueError: If the format is not supported.
        """
        with open(file_path, 'r') as file:
            content = file.read()
            if format == 'json':
                return cls.from_json(content)
            elif format == 'yaml':
                return cls.from_yaml(content)
            else:
                raise ValueError("Unsupported format. Use 'json' or 'yaml'.")

    @staticmethod
    def validate_serialized_data(data, format='json'):
        """
        Validate if the given data is a valid serialized string in the specified format.

        :param data: Serialized string to validate.
        :param format: Format of the serialization ('json' or 'yaml').
        :return: True if the data is valid, False otherwise.
        :raise ValueError: If the format is not supported.
        """
        try:
            if format == 'json':
                json.loads(data)
            elif format == 'yaml':
                yaml.safe_load(data)
            else:
                raise ValueError("Unsupported format. Use 'json' or 'yaml'.")
            return True
        except (json.JSONDecodeError, yaml.YAMLError):
            return False


class BasicSingleton:
    """
    A mix-in class to implement the singleton pattern.
    Ensures that only one instance of the class exists.
    """
    _instances = {}

    def __new__(cls, *args, **kwargs):
        """
        Create a new instance of the class if it does not exist, otherwise return the existing instance.

        :return: The single instance of the class.
        """
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ObservableMixin:
    """
    A mix-in class to implement the observer pattern.
    Allows objects to be observed by other objects.
    """

    def __init__(self):
        """
        Initialize the observable object with an empty list of observers.
        """
        self._observers = []

    def add_observer(self, observer):
        """
        Add an observer to the list of observers.

        :param observer: The observer to add.
        """
        self._observers.append(observer)

    def remove_observer(self, observer):
        """
        Remove an observer from the list of observers.

        :param observer: The observer to remove.
        """
        self._observers.remove(observer)

    def notify_observers(self, *args, **kwargs):
        """
        Notify all observers of an event.



        :param args: Positional arguments to pass to the observers.
        :param kwargs: Keyword arguments to pass to the observers.
        """
        for observer in self._observers:
            observer.spots(*args, **kwargs)


class ReprMixin:
    """
    A mix-in class to provide a custom `__repr__` method.
    Generates a string representation of the instance with its class name and attributes.
    """

    def __repr__(self):
        """
        Generate a string representation of the instance.

        :return: A string representation of the instance.
        """
        class_name = self.__class__.__name__
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{class_name}({attrs})"