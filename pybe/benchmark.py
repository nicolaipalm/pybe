from typing import List, Callable, Dict, Union, Optional
import pandas as pd
from tqdm import tqdm
import multiprocessing as mp


class Benchmark:
    """Benchmark any Python function

    pybe.Benchmark allows you to:

    * **benchmark** any Python function (with vectors of real numbers as output)

    * **store** the results in a csv (default) or excel file and

    * **read** from previous benchmark results.

    .. epigraph::
        **How it works:**
        Specify a list of inputs and apply a given function to those inputs a specified number of times
    """

    def __init__(self,
                 benchmark_csv_file_path: Optional[str] = None,
                 ):
        if benchmark_csv_file_path is not None:
            self.read_from_csv(benchmark_csv_file_path)

    def __call__(self,
                 function: Callable[..., Dict[str, float]],
                 inputs: List[Union[str, float]],
                 name: str,
                 number_runs: int = 10,
                 store: bool = True,
                 parallel: bool = False,
                 ):
        """Benchmark a function


        Parameters
        ----------
        function : Callable[..., Dict[str, float]]
            function to be benchmarked which returns a dictionary with keys the _name of the output (string)
            and value the value of the function (float)

        inputs : List[Union[str, float]]
            inputs on which the function is to be benchmarked stored as a list of strings or floats

        number_runs : int
            number of runs for each inputs

        store : bool
            if true, store the output of the benchmark as a benchmark.yaml

        parallel : bool
            if true, run the benchmark on parallel (using multiprocessing)


        Examples
        --------
        Initialize the benchmark class.

        >>> benchmark = Benchmark()

        Define the function to be benchmarked. This function must take a single argument (float or string) and return
        a dictionary where each key represents one output

        >>> def test_function(i: int):
        >>>     return {"value": i}

        Define the list of inputs

        >>> inputs = [1, 2, 3]

        Specify the number of runs

        >>> number_runs=3

        Run the benchmark

        >>> benchmark(function=test_function,
        ...           name="test-benchmark",
        ...           inputs=inputs,
        ...           number_runs=number_runs)
        """

        self._name = name
        self._inputs = inputs

        # TODO: test what if dict contains numpy array or others...
        if parallel:
            for x in tqdm(inputs):
                # TODO: doesnt work for generating instances of classes
                try:
                    with mp.Pool() as pool:
                        results_x = pool.map(function, [x for _ in range(number_runs)])
                    # re-arrange results
                    self._result[x] = {key: [value[key] for value in results_x] for key in results_x[0].keys()}

                except RuntimeError:
                    print("benchmark(test_function) needs to be inside the if __name__ == '__main__': "
                          'clause to prevent spawning infinite processes.')
                    break

        else:
            self._result = []
            for x in tqdm(inputs):
                for _ in range(number_runs):
                    result_x = function(x)
                    result_x['Input'] = x
                    result_x['Name'] = name
                    self._result.append(result_x)
        self._name_outputs = list(result_x.keys())
        self._result = pd.concat([pd.DataFrame(result, index=[0]) for result in self._result], ignore_index=True)

        if store:
            self.to_csv(name)

    def to_excel(self, name: str = 'benchmark'):
        """Save results to excel (xlsx) file (file path is file path of script)

        Parameters
        ----------
        name : str
            name of the benchmark
        """
        self.result.to_excel(f'{name}.xlsx')

    def to_csv(self, name: str = 'benchmark'):
        """Save results to csv file (file path is file path of script)

        Parameters
        ----------
        name : str
            name of the benchmark
        """
        self.result.to_csv(f'{name}.csv', index=False)

    @property
    def result(self) -> pd.DataFrame:
        """Return the result of the benchmark as a pandas DataFrame

        Returns
        -------
        pd.DataFrame
            result of the benchmark

        """
        return self._result

    def read_from_csv(self, benchmark_csv_file_path: str):
        """Read previous results of corresponding yaml file and store them in this instance

        Parameters
        ----------
        benchmark_csv_file_path : str
            path of benchmark yaml file

        Examples
        --------
        >>> benchmark = Benchmark() # initialize benchmark instance
        >>> benchmark.read_from_csv(benchmark_csv_file_path="./benchmark.csv") # read results
        >>> print(benchmark.result) # print result
        """
        self._result = pd.read_csv(benchmark_csv_file_path)

    def return_outputs(self, input: float):
        return self.result.loc[self.result['Input'] == input]

    @property
    def inputs(self) -> List[Union[str, float]]:
        """Return the list of inputs of the benchmark

        Returns
        -------
        List[Union[str, float]]
            inputs of the benchmark

        """
        return list(set(self.result['Input'].values))

    @property
    def name_outputs(self) -> List[str]:
        """Return the list of names of outputs of the benchmark

        Returns
        -------
        List[str]
            name of outputs

        """
        return list(self.result.columns.drop(['Input', 'Name']))

    @property
    def means(self) -> pd.DataFrame:
        """Return the means of the outputs as pandas DataFrame

        Returns
        -------
        pd.DataFrame
            means of the benchmark

        """
        means = self.result.groupby(['Input']).mean(numeric_only=True).reset_index()
        means['Name'] = self.name
        return means

    @property
    def std(self) -> pd.DataFrame:
        """Return the standard deviation of the outputs as pandas DataFrame

        Returns
        -------
        pd.DataFrame
            std of the benchmark

        """
        std = self.result.groupby(['Input']).std(numeric_only=True).reset_index()
        std['Name'] = self.name
        return std

    @property
    def name(self) -> str:
        """Return the name of the benchmark

        Returns
        -------
        str
            name of the benchmark

        """
        return self.result['Name'].values[0]
