import time
from functools import wraps


def timer(func):
    @wraps(func)
    def function_with_timer(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        result["time"] = total_time
        return result

    return function_with_timer
