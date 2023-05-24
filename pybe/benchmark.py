from typing import List, Callable, Dict, Union, Optional

import pandas as pd
from tqdm import tqdm
import yaml
import multiprocessing as mp


class Benchmark:
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
        with open(f"{name}.yaml", "w") as f:
            yaml.dump({"Meta": self.meta, "Result": self.result}, f)

    def to_excel(self, name: str = "benchmark"):
        self.result_data_frame.to_excel(f"{name}.xlsx")

    def to_csv(self, name: str = "benchmark"):
        self.result_data_frame.to_csv(f"{name}.csv")

    @property
    def result_data_frame(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(
            {("Input: " + str(input), "Output: " + str(output_name)): {("Iteration", i + 1): value for i, value in
                                                                       enumerate(self.result[input][output_name])}
             for input in self.result.keys()
             for output_name in self.result[input].keys()},
            orient='index')

    def read_from_yaml(self, benchmark_yaml_file_path: str):
        try:
            with open(benchmark_yaml_file_path) as f:
                content = yaml.load(f, Loader=yaml.FullLoader)
                self.meta = content.get("Meta")
                self.result = content.get("Result")
        except:
            print("Something went wrong when reading the benchmark yaml file.")

    @property
    def inputs(self) -> List[Union[str, float]]:
        return list(self.result.keys())

    @property
    def name_outputs(self) -> List[str]:
        return list(self.result[self.inputs[0]].keys())
