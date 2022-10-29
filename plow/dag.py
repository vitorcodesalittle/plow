from typing import Any, Callable, List, Optional
from pydantic import BaseModel

StepSchema = Any ## TODO: Generate NodeType Union

class Dag(BaseModel):
    name: str
    inputs: Any
    steps: List[StepSchema]
    # TODO: fill the return type of the dag run

    def run(self, inputs: dict[str, Any]) -> Any:
        ...

    def iterate_toposort(self, fn: Callable[[StepSchema, dict[str, Any]], None]):
        ...


def make_dag(yaml_str: Optional[str] = None) -> Dag:
    ...
