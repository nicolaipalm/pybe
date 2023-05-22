from typing import List, Callable, Any, Dict

import tqdm as tqdm
import yaml


class Benchmark:
    def __init__(self,
                 inputs: List,
                 meta_data: Dict,
                 store: bool = True,
                 statistical: bool = False,
                 ):
        self._meta_data = meta_data
        self._store = store
        self._statistical = statistical
        self.inputs = inputs
        self.result = {
        }

        if statistical:
            self.result["Mean"] = []
            self.result["Std"] = []

    def __call__(self,
                 function: Callable[..., Dict]
                 ):
        # TODO: test what if dict contains numpy array or others...
        for input in tqdm(self.inputs):
            self.result[input] = function(input)

        if self._store:
            self.store()

    def store(self):
        with open(f"benchmark.yaml", "w") as f:
            yaml.dump({"Meta": self._meta_data, "Result": self.result}, f)

    def calculate_mean(self):
        return None

    def calculate_std(self):
        return None
