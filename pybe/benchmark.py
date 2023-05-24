from typing import List, Callable, Dict, Union, Optional

import pandas as pd
from tqdm import tqdm
import yaml
import multiprocessing as mp


class Benchmark:
    """Benchmark any Python function

    This class lets you
    - bootstrap any Python function
    - store the results in a yaml, excel or csv file
    - convert them into a pandas data frame
    - read from previous benchmark results.

    .. epigraph::
        **How it works:**
        Specify a list of inputs and apply a given function to those inputs a specified number of times
    """

    def __init__(self,
                 benchmark_yaml_file_path: Optional[str] = None,
                 ):
        if benchmark_yaml_file_path is not None:
            self.read_from_yaml(benchmark_yaml_file_path)

    def __call__(self,
                 function: Callable[..., Dict[Union[str, float], float]],
                 inputs: List[Union[str, float]],
                 meta_data: Dict,
                 number_runs: int = 10,
                 store: bool = True,
                 parallel: bool = False,
                 ):
        """Benchmark a function


        Parameters
        ----------
        function : Callable[..., Dict[Union[str, float], float]]
            function to be benchmarked which takes either a string or float as input and returns a float as output

        inputs : List[Union[str, float]]
            inputs on which the function is to be benchmarked stored as a list of strings or floats

        meta_data : dict
            all meta data of the benchmark stored as a dictionary

        number_runs : int
            number of runs for each inputs

        store : bool
            if true, store the output of the benchmark as a benchmark.yaml

        parallel : bool
            if true, run the benchmark on parallel (using multiprocessing)


        Examples
        --------
        Initialize the benchmark class.

        benchmark = Benchmark()

        Define the function to be benchmarked. This function must take a single argument (float or string) and return
        a dictionary where each key represents one output

        >>> def test_function(i: int):
        >>>     return {"value": i}

        Define the list of inputs

        >>> inputs = [1, 2, 3]

        Specify the number of runs

        >>> number_runs=3

        Store the meta information about the benchmark as a dictionary

        >>> meta_data = {"Name": "Test","Place":"Gringots"}

        Run the benchmark

        >>> benchmark(function=test_function,
        ...           meta_data=meta_data,
        ...           inputs=inputs,
        ...           number_runs=number_runs)
        """

        self.meta = meta_data
        self.result = {
        }

        # TODO: test what if dict contains numpy array or others...
        if parallel:
            for x in tqdm(inputs):
                # TODO: doesnt work for generating instances of classes
                try:
                    with mp.Pool() as pool:
                        results_x = pool.map(function, [x for _ in range(number_runs)])
                    # re-arrange results
                    self.result[x] = {key: [value[key] for value in results_x] for key in results_x[0].keys()}
                except RuntimeError:
                    print("benchmark(test_function) needs to be inside the if __name__ == '__main__': "
                          "clause to prevent spawning infinite processes.")
                    break

        else:
            for x in tqdm(inputs):
                results_x = [function(x) for _ in range(number_runs)]
                # re-arrange results
                self.result[x] = {key: [value[key] for value in results_x] for key in results_x[0].keys()}

        if store:
            self.to_yaml()

    def to_yaml(self, name: str = "benchmark"):
        """Save results to yaml file

        Parameters
        ----------
        name : str
            name of the benchmark
        """
        with open(f"{name}.yaml", "w") as f:
            yaml.dump({"Meta": self.meta, "Result": self.result}, f)

    def to_excel(self, name: str = "benchmark"):
        """Save results to excel (xlsx) file

        Parameters
        ----------
        name : str
            name of the benchmark
        """
        self.result_data_frame.to_excel(f"{name}.xlsx")

    def to_csv(self, name: str = "benchmark"):
        """Save results to csv file

        Parameters
        ----------
        name : str
            name of the benchmark
        """
        self.result_data_frame.to_csv(f"{name}.csv")

    @property
    def result_data_frame(self) -> pd.DataFrame:
        """Return the result of the benchmark as a pandas DataFrame

        Returns
        -------
        pd.DataFrame
            result of the benchmark

        """
        return pd.DataFrame.from_dict(
            {("Input: " + str(input), "Output: " + str(output_name)): {("Iteration", i + 1): value for i, value in
                                                                       enumerate(self.result[input][output_name])}
             for input in self.result.keys()
             for output_name in self.result[input].keys()},
            orient='index')

    def read_from_yaml(self, benchmark_yaml_file_path: str):
        """Read previous results of corresponding yaml file and store them in this instance

        Parameters
        ----------
        benchmark_yaml_file_path : str
            path of benchmark yaml file

        Examples
        --------
        >>> benchmark = Benchmark() # initialize benchmark instance
        >>> benchmark.read_from_yaml(benchmark_yaml_file_path="./benchmark.yaml") # read results
        >>> print(benchmark.inputs) # print inputs
        """
        try:
            with open(benchmark_yaml_file_path) as f:
                content = yaml.load(f, Loader=yaml.FullLoader)
                self.meta = content.get("Meta")
                self.result = content.get("Result")
        except:
            print("Something went wrong when reading the benchmark yaml file.")

    @property
    def inputs(self) -> List[Union[str, float]]:
        """Return the given inputs of the benchmark

        Returns
        -------
        List[Union[str, float]]
            input of benchmark
        """
        return list(self.result.keys())

    @property
    def name_outputs(self) -> List[str]:
        """Return the names (i.e. keys) of the outputs of the benchmark

        Returns
        -------
        List[Union[str, float]]
            name of outputs of benchmark
        """
        return list(self.result[self.inputs[0]].keys())
