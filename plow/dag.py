import graphlib
from pprint import pprint
import yaml
from pathlib import Path
from typing import Any, Callable, List, Optional, Union
from pydantic import BaseModel

class StepSchema(BaseModel):
    alias: str
    type: str # TODO: narrow it to Literal?
    args: Any # TODO: narrow it to object

class Dag(BaseModel):
    name: str
    inputs: Any
    steps: List[StepSchema]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _process(self, step: StepSchema):
        pprint(step)

    def run(self, inputs: dict[str, Any]) -> Any:
        self.iterate_toposort(lambda s: self._process(s))

    def iterate_toposort(self, fn: Callable[[StepSchema], None]):
        sorter = graphlib.TopologicalSorter()
        steps_by_alias = {
                step.alias: step for step in self.steps
                }
        for step in self.steps:
            sorter.add(step.alias)
        nodes = sorter.static_order()
        for step_alias in nodes:
            step = steps_by_alias[step_alias]
            fn(step)


def make_dag(*, yaml_path: Optional[Union[Path, str]] = None, yaml_str: Optional[str] = None) -> Dag:
    assert yaml_str or yaml_path, "yaml_str or yaml_path is required"
    yaml_values = {}
    if yaml_str:
        yaml_values = yaml.unsafe_load(yaml_str)
    elif yaml_path:
        with open(yaml_path, 'rb') as f:
            yaml_values = yaml.unsafe_load(f)
    return Dag(**yaml_values)

