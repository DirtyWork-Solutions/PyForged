import time

class TimingMixin:
    def time_method(self, method, *args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time of {method.__name__}: {end_time - start_time} seconds")
        return result