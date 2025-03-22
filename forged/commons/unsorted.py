import threading

import time
from functools import wraps

def retry(retries=3, delay=1):
        """
        A decorator that retries a function execution a specified number of times with a delay between each attempt.

        Parameters:
        retries (int): The number of times to retry the function. Default is 3.
        delay (int or float): The delay in seconds between each retry attempt. Default is 1 second.

        Returns:
        function: The wrapped function with retry logic.

        Example:
        @retry(retries=5, delay=2)
        def unstable_function():
            # Function logic that might raise an exception
            pass
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt < retries - 1:
                            time.sleep(delay)
                        else:
                            raise e
            return wrapper
        return decorator