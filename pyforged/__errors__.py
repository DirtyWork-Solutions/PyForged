import time
from functools import wraps
from typing import Callable


# 4.1 Unified Exception Base Class
class PyForagedException(Exception):
    """Base exception class for all PyForaged errors."""
    pass

# 4.2 Exception Decorators
def exception_handler(default_return=None):
    """Decorator to catch exceptions and return a default value."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Exception in {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator

# 4.3 Retry Mechanism
def retry(times=3, delay=1):
    """Retry decorator with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Retry {attempt+1}/{times} for {func.__name__}: {e}")
                    time.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator

# 4.4 Circuit Breaker Pattern
class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_time=10):
        self.failure_threshold = failure_threshold
        self.reset_time = reset_time
        self.failures = 0
        self.last_attempt = 0

    def is_open(self):
        return self.failures >= self.failure_threshold and (time.time() - self.last_attempt) < self.reset_time

    def call(self, func, *args, **kwargs):
        if self.is_open():
            raise PyForagedException("Circuit breaker is open")
        try:
            result = func(*args, **kwargs)
            self.failures = 0  # Reset on success
            return result
        except Exception:
            self.failures += 1
            self.last_attempt = time.time()
            raise

# 4.5 Failover Handler
def failover(primary: Callable, secondary: Callable):
    """Try primary function, fallback to secondary if it fails."""
    try:
        return primary()
    except Exception:
        return secondary()

# 4.6 Error Aggregator
class ErrorAggregator:
    """Aggregates multiple errors and raises them together."""
    def __init__(self):
        self.errors = []

    def add(self, error: Exception):
        self.errors.append(error)

    def raise_if_any(self):
        if self.errors:
            raise PyForagedException(self.errors)