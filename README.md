[Visualization](https://nicolaipalm-pybe-dashboard-dashboard-yb61qz.streamlit.app) //
[Documentation](https://pybe.readthedocs.io/en/latest/source/benchmark.html)

# PyBe - benchmark your Python functions

Benchmark any (Python) function, store (as csv or Excel), read and [visualize](https://nicolaipalm-pybe-dashboard-dashboard-yb61qz.streamlit.app)
the results with only a few lines of code!

*Table of Contents:*
1. [Structure of a benchmark](#structure-of-a-benchmark)
2. [Installation](#installation)
3. [Getting started](#getting-started)
4. [Structure of csv](#structure-of-benchmark-csv)

## Structure of a benchmark

The general structure of a benchmark script is as follows:
- you have some algorithm
- you want to test the algorithm by varying over a set of inputs
- you assess quantities of interest (i.e. some performance metric) to the output of the algorithm

This can be implemented as a Python function:

    def benchmark_function(input):
        result = algorithm(input)
        return {"name_performance_metric_1": performance_metric_1(result),"name_performance_metric_2": performance_metric_1(result),...}


In order to benchmark your algorithm you simply need to call the above function to all sets of inputs.
This and [storing your results](#structure-of-benchmark-csv) is taken care of by the Benchmark class in pybe.benchmark.
Lets look at a concrete example.

### Example: Optimization algorithm
Lets say you have an optimization algorithm implemented in Python
which takes as inputs
- a function to be optimized and
- the number of runs.

You want to evaluate the optimizer on a certain test function and benchmark how well the optimizer
performs for specific number of runs.
For this you have a performance metric which can be called to the output of the optimization and returns
a real number (float).

Then, your benchmark function looks as follows:

    def benchmark_function(number_of_runs):
        result_optimizer = optimizer(test_function,number_of_runs)
        return {"name_performance_metric": performance_metric(result_optimizer)}

Lets say you want to benchmark your optimization algorithm for number of runs 10,100 and 1000.
Now, you can simply benchmark your optimization algorithm by using the pybe Benchmark class.

    from pybe.benchmark import Benchmark
    benchmark = Benchmark()
    benchmark(function=benchmark_function,inputs=[10,100,1000],name="name_of_my_optimization_algorithm")

Drag the resulting **name_of_my_optimization_algorithm.csv** into the [Dashboard](https://nicolaipalm-pybe-dashboard-dashboard-yb61qz.streamlit.app) and thats it!

## Installation
The official release is available at PyPi:

```
pip install pybe
```

You can clone this repository by running the following command:

```
git clone https://github.com/nicolaipalm/pybe
cd pybe
pip install
```

## Getting started

In order to benchmark a Python function you only need to implement the function and
specify some data of the benchmark.

```python
from pybe.benchmark import Benchmark
from pybe.wrappers import timer
import time

benchmark = Benchmark() # initialize pybe's benchmark class


@timer # additionally track the time needed in each iteration
def test_function(i: int):
    time.sleep(0.1)
    return {"name_of_output": i} # specify the output in a dictionary

# benchmark test_function on inputs [1,2,3] and evaluate each input 10 times
benchmark(test_function,
          name="test_benchmark", # set the name of the benchmark
          inputs=[1, 2, 3],
          store=True, # store the benchmark results
          number_runs=10)
```
Look at the benchmark.csv file in your directory!

You can view the results also directly in Python or write them to an Excel or csv file

```python
print(benchmark.inputs, benchmark.name_outputs)  # print inputs and names of outputs
print(benchmark.result)  # print results as stored in benchmark.csv
benchmark.to_excel(name="my_results")  # write results as excel
benchmark.to_csv(name="my_results")  # write results as csv

```

You can read any of the benchmark results by simply initializing the
benchmark class with parameter the .yaml benchmark file path

```python
benchmark = Benchmark(benchmark_file_path)
```

## Structure of benchmark csv

The structure of the resulting csv is supposed to be very intuitive:
- each row represents one call of the benchmarked function with
- one column for the input
- one column with the name of the benchmark
- one column for each output

For example:
- the function has two outputs: time and value
- is benchmarked at inputs 10 and 100
- has name Hello
- is evaluated once for each input

Then, the resulting csv/Excel has the following structure:

|   | value    | time  | Input | Name |
|---|----------|-------|-------|------|
| 0 | 0.1      | 1     | 10    | hello|
| 1 | 0.05     | 20    | 100   | hello|

## Dashboard

[You can easily visualize your benchmark results!](https://nicolaipalm-pybe-dashboard-dashboard-yb61qz.streamlit.app)
