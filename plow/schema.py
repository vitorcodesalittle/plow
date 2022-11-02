from typing import Union
from pydantic.main import BaseModel


class AddArgs(BaseModel):
    a: float
    b: float


class AddStep(BaseModel):
    alias: str
    type = "add"
    args: AddArgs


class SubArgs(BaseModel):
    a: float
    b: float


class SubStep(BaseModel):
    alias: str
    type = "add"
    args: AddArgs


Step = Union[AddStep, SubStep]
