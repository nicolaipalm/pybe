from pybe.benchmark import Benchmark

benchmark = Benchmark('./benchmark.csv')


if __name__ == '__main__':
    print(benchmark.name)
    print(benchmark.name_outputs)
    print(benchmark.result.mean(numeric_only=True))
