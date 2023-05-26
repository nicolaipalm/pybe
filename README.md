[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/jkanner/streamlit-audio/main/app.py)

# PyBe - benchmark your Python functions

Benchmark any (scientific) function which outputs floats, store (as yaml, csv or excel)
and read the results with only a few lines of code.

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
benchmark(test_function,meta_data={"Name": "Test"}, # set meta data of benchmark
          inputs=[1, 2, 3],
          store=True, # store the benchmark results
          number_runs=10)
```
Look at the benchmark.yaml file in your directory!

You can view the results also directly in Python or write them to an excel or csv file

```python
print(benchmark.inputs, benchmark.name_outputs)  # print inputs and names of outputs
print(benchmark.result)  # print results as stored in benchmark.csv
benchmark.to_excel(name="my_results")  # write results as excel
benchmark.to_csv(name="my_results")  # write results as csv

```

You can read any of the benchmark results by simply initializing the
benchmark class with parameter the .yaml benchmark file path

```python
benchmark = Benchmark(benchmark__file_path)
```
## Structure of benchmark csv

## Dashboard
(Dashboard link)
