"""
This module provides various utilities for error handling and resilience patterns, including custom exceptions, decorators for exception handling and retries, a circuit breaker implementation, and error aggregation and cataloging.

Classes:
    - CustomException: Base exception class for all PyForaged errors.
    - PyForgedException: Specific exception class for PyForaged errors.
    - CircuitBreaker: Implements the circuit breaker pattern to prevent repeated failures.
    - ErrorAggregator: Aggregates multiple errors and raises them together.
    - ErrorCatalogue: Manages error codes and messages in a catalogue.

Functions:
    - exception_handler: Decorator to catch exceptions and return a default value.
    - retry: Decorator to retry a function with exponential backoff.
     - failover: Tries a primary function and falls back to a secondary function if the primary fails.
"""

import json
from functools import wraps
import time
from logging import ERROR
from typing import Callable, Tuple
from loguru import logger as log
import threading

class CustomException(Exception):
    """
    Base exception class for all PyForaged errors.

    Attributes:
        msg (str): The error message.
        code (int): The error code.
        log_exception (bool): Whether to log the exception.
        level (Warning): The warning level.
        context (dict): The context of the error.
        is_logged (bool): Whether the error is logged.
    """

    def __init__(self, msg, code=-1, log_exception: bool = True, *args, **kwargs):
        self.msg = msg
        super().__init__(self.msg)
        self.level = ERROR
        self.context = {}
        self.code = code
        self.is_logged = log_exception

class PyForgedException(CustomException):
    """
    Base exception class for all PyForaged errors.
    """
    def __init__(self, msg):
        super().__init__(msg)

def exception_handler(default_return=None):
    """
    Decorator to catch exceptions and return a default value.

    Args:
        default_return: The default value to return if an exception occurs.

    Returns:
        The decorated function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log.exception(f"Exception in {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator

def retry(times=3, delay=1):
    """
    Retry decorator with exponential backoff.

    Args:
        times (int): The number of retry attempts.
        delay (int): The initial delay between retries.

    Returns:
        The decorated function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    log.error(f"Retry {attempt+1}/{times} for {func.__name__}: {e}")
                    time.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator


# CircuitBreaker class
class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_time=10, success_threshold=2, exception_types=(Exception,), on_state_change: Callable[[str, str], None] = None):
        self.failure_threshold = failure_threshold
        self.reset_time = reset_time
        self.success_threshold = success_threshold
        self.failures = 0
        self.successes = 0
        self.last_attempt = 0
        self.state = 'closed'
        self.exception_types = exception_types
        self.lock = threading.Lock()
        self.on_state_change = on_state_change

    def _change_state(self, new_state: str):
        old_state = self.state
        self.state = new_state
        if self.on_state_change:
            self.on_state_change(old_state, new_state)

    def is_open(self):
        with self.lock:
            if self.state == 'open' and (time.time() - self.last_attempt) >= self.reset_time:
                self._change_state('half-open')
            return self.state == 'open'

    def call(self, func, *args, **kwargs):
        with self.lock:
            if self.is_open():
                raise PyForgedException("The circuit breaker is open.")
            if self.state == 'half-open':
                self._change_state('closed')

        try:
            result = func(*args, **kwargs)
            with self.lock:
                if self.state == 'half-open':
                    self.successes += 1
                    if self.successes >= self.success_threshold:
                        self._change_state('closed')
                        self.failures = 0
                        self.successes = 0
                else:
                    self.failures = 0  # Reset on success
            return result
        except self.exception_types as e:
            with self.lock:
                self.failures += 1
                self.last_attempt = time.time()
                if self.failures >= self.failure_threshold:
                    self._change_state('open')
            raise PyForgedException(f"Function call failed: {e}")

def failover(primary: Callable, secondary: Callable):
    """
    Try primary function, fallback to secondary if it fails.

    Args:
        primary (Callable): The primary function to call.
        secondary (Callable): The secondary function to call if the primary fails.

    Returns:
        The result of the primary or secondary function.
    """
    try:
        return primary()
    except Exception:
        return secondary()

class ErrorAggregator:
    """
    Aggregates multiple errors and raises them together.

    Attributes:
        errors (list): The list of errors.
    """
    def __init__(self):
        self.errors = []

    def add(self, error: Exception):
        """
        Add an error to the aggregator.

        Args:
            error (Exception): The error to add.
        """
        self.errors.append(error)

    def raise_if_any(self):
        """
        Raise all aggregated errors if any exist.

        Raises:
            PyForgedException: If there are any aggregated errors.
        """
        if self.errors:
            raise PyForgedException(str(self.errors))

class ErrorCatalogue:
    """
    Catalogue for managing error codes and messages.

    Attributes:
        catalogue (dict): The dictionary of error codes and messages.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ErrorCatalogue, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'catalogue'):
            self.catalogue = {}

    def add_error(self, error_code: str, error_message: str):
        """
        Add an error to the catalogue.

        Args:
            error_code (str): The error code.
            error_message (str): The error message.
        """
        self.catalogue[error_code] = error_message

    def update_error_message(self, error_code: str, new_message: str):
        """
        Update the message for an existing error code.

        Args:
            error_code (str): The error code.
            new_message (str): The new error message.

        Raises:
            KeyError: If the error code is not found.
        """
        if error_code in self.catalogue:
            self.catalogue[error_code] = new_message
        else:
            raise KeyError(f"Error code {error_code} not found in the catalogue")

    def get_error(self, error_code: str) -> str:
        """
        Get the message for an error code.

        Args:
            error_code (str): The error code.

        Returns:
            str: The error message.
        """
        return self.catalogue.get(error_code, "Unknown error code")

    def remove_error(self, error_code: str):
        """
        Remove an error from the catalogue.

        Args:
            error_code (str): The error code.
        """
        if error_code in self.catalogue:
            del self.catalogue[error_code]

    def list_errors(self) -> dict:
        """
        List all errors in the catalogue.

        Returns:
            dict: The dictionary of error codes and messages.
        """
        return self.catalogue

    def search_errors_by_message(self, search_term: str) -> dict:
        """
        Search for errors by message.

        Args:
            search_term (str): The term to search for in error messages.

        Returns:
            dict: The dictionary of matching error codes and messages.
        """
        return {code: msg for code, msg in self.catalogue.items() if search_term in msg}

    def error_exists(self, error_code: str) -> bool:
        """
        Check if an error code exists in the catalogue.

        Args:
            error_code (str): The error code.

        Returns:
            bool: True if the error code exists, False otherwise.
        """
        return error_code in self.catalogue

    def import_from_json(self, file_path: str):
        """
        Import errors from a JSON file.

        Args:
            file_path (str): The path to the JSON file.
        """
        with open(file_path, 'r') as file:
            self.catalogue = json.load(file)

    def add_error_category(self, error_code: str, category: str):
        """
        Add a category to an error.

        Args:
            error_code (str): The error code.
            category (str): The category to add.

        Raises:
            KeyError: If the error code is not found.
        """
        if error_code in self.catalogue:
            self.catalogue[error_code] = {"message": self.catalogue[error_code], "category": category}
        else:
            raise KeyError(f"Error code {error_code} not found in the catalogue")

    def get_errors_by_category(self, category: str) -> dict:
        """
        Get errors by category.

        Args:
            category (str): The category to filter by.

        Returns:
            dict: The dictionary of error codes and messages in the category.
        """
        return {code: details["message"] for code, details in self.catalogue.items() if
                details.get("category") == category}

    def list_categories(self) -> set:
        """
        List all categories in the catalogue.

        Returns:
            set: The set of categories.
        """
        return {details.get("category") for details in self.catalogue.values() if isinstance(details, dict)}