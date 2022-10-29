import graphlib
import yaml
from pathlib import Path
from typing import Any, Callable, List, Optional, Union
from pydantic import BaseModel
from plow.decorators import get_func


class StepSchema(BaseModel):
    alias: str
    type: str  # TODO: narrow it to Literal?
    args: Any  # TODO: narrow it to object


class Dag(BaseModel):
    name: str
    inputs: Any
    steps: List[StepSchema]
    _mem = {}
    steps_by_alias: dict[str, StepSchema] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.steps_by_alias = {step.alias: step for step in self.steps}
        for key, v in self.inputs.items():
            self._mem[f"inputs.{key}"] = v

    def _read(self, key: Any) -> Any:
        if isinstance(key, str):
            if self._is_reference(key):  # TODO handle ${...} cases
                return self._mem[self._unwrap_dollar(key)]  # read as reference
        return key  # read as the value loaded by yaml TODO: support structured data

    def _process(self, step: StepSchema):
        func = get_func(func_name=step.type)
        callable = func.ref()
        if isinstance(step.args, dict):
            args = {
                arg_name: self._read(arg_value)
                for arg_name, arg_value in step.args.items()
            }
            self._mem[step.alias] = callable(**args)
        elif isinstance(step.args, list):
            args = [self._read(arg_value) for arg_value in step.args]
            self._mem[step.alias] = callable(*args)

    def run(self, inputs: dict[str, Any]) -> Any:
        self.iterate_toposort(lambda s: self._process(s))
        return self._mem  # TODO: return more meaningful output

    def _is_input(self, value: Any):
        return self._is_reference(value) and self._unwrap_dollar(value).startswith(
            "inputs."
        )

    def _is_reference(self, value: Any):
        return isinstance(value, str) and value.startswith("$")

    def _unwrap_dollar(self, value: Any):
        return value[1:]

    def _get_outgoing_steps(self, step_name):
        step = self.steps_by_alias[step_name]
        arg_values = step.args.values() if isinstance(step, dict) else step.args
        refs = []
        for value in arg_values:
            if self._is_reference(value) and not self._is_input(value):
                refs.append(self._unwrap_dollar(value))
        return refs

    def iterate_toposort(self, fn: Callable[[StepSchema], None]):
        sorter = graphlib.TopologicalSorter()

        for step in self.steps:
            outgoing = self._get_outgoing_steps(step.alias)
            sorter.add(step.alias, *outgoing)
        nodes = sorter.static_order()
        for step_alias in nodes:
            step = self.steps_by_alias[step_alias]
            fn(step)


def make_dag(
    *, yaml_path: Optional[Union[Path, str]] = None, yaml_str: Optional[str] = None
) -> Dag:
    assert yaml_str or yaml_path, "yaml_str or yaml_path is required"
    yaml_values = {}
    if yaml_str:
        yaml_values = yaml.unsafe_load(yaml_str)
    elif yaml_path:
        with open(yaml_path, "rb") as f:
            yaml_values = yaml.unsafe_load(f)
    return Dag(**yaml_values)
