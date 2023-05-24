"""Decorator for the function to be benchmarked

Includes
- time (track time for each iteration)

"""

import time
from functools import wraps


def timer(func):
    """Track the time needed for each iteration

    Store the time needed as additional output with name (i.e. key) "time"

    Parameters
    ----------
    func : Callable[..., Dict[Union[str, float], float]]
        function to be benchmarked which takes either a string or float as input and returns a float as output

    Returns
    -------
    Callable[..., Dict[Union[str, float], float]]
        function to be benchmarked with additional time needed output
    """
    @wraps(func)
    def function_with_timer(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        result["time"] = total_time
        return result

    return function_with_timer
