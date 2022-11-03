from typing import List, Union
from pydantic.main import BaseModel


class AddArgs(BaseModel):
    a: float
    b: float


class AddStep(BaseModel):
    alias: str
    type = "add"
    args: AddArgs | List[str]


class SubArgs(BaseModel):
    a: float
    b: float


class SubStep(BaseModel):
    alias: str
    type = "add"
    args: AddArgs


Step = Union[AddStep, SubStep]
