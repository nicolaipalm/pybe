import time

from pybe.benchmark import Benchmark
from pybe.wrappers import timer

benchmark = Benchmark()


@timer
def function(i: int):
    time.sleep(0.1)
    return {'value': i}


if __name__ == '__main__':
    benchmark(function, name='test_benchmark', inputs=[1, 2, 3], number_runs=3, store=True)
    print(benchmark.name)
    print(benchmark.name_outputs)
    print(benchmark.result.mean(numeric_only=True))
