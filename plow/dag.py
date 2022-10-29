import yaml
from pathlib import Path
from typing import Any, Callable, List, Optional, Union
from pydantic import BaseModel

StepSchema = Any ## TODO: Generate NodeType Union

class Dag(BaseModel):
    name: str
    inputs: Any
    steps: List[StepSchema]

    def run(self, inputs: dict[str, Any]) -> Any:
        ...

    def iterate_toposort(self, fn: Callable[[StepSchema, dict[str, Any]], None]):
        ...


def make_dag(*, yaml_path: Optional[Union[Path, str]] = None, yaml_str: Optional[str] = None) -> Dag:
    assert yaml_str or yaml_path, "yaml_str or yaml_path is required"
    yaml_values = {}
    if yaml_str:
        yaml_values = yaml.unsafe_load(yaml_str)
    elif yaml_path:
        with open(yaml_path, 'rb') as f:
            yaml_values = yaml.unsafe_load(f)
    return Dag(**yaml_values)

