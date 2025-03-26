from abc import ABC, abstractmethod


class BaseCustomException(ABC, Exception):
    """
    Base class for custom exceptions
    """
    @abstractmethod
    def __init__(self, message: str):
        pass

class PyForgedException(BaseCustomException):
    def __init__(self, message: str = None):
        self.message = message if message else 'An error occurred with the Namespacing component.'

class NamespacingException(PyForgedException):
    def __init__(self, message: str = None):
        self.message = message if message else 'An error occurred with the Namespacing component.'

class ConfiguredException(PyForgedException):
    def __init__(self, message: str = None):
        self.message = message if message else 'An error occurred with the Configured component.'

class EventsException(PyForgedException):
    def __init__(self, message: str = None):
        self.message = message if message else 'An error occurred with the Events & Signalling component.'

class HooksException(PyForgedException):
    def __init__(self, message: str = None):
        self.message = message if message else 'An error occurred with the Hooks & Extensibility component.'

# TODO: add module hooks