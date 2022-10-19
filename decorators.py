from inspect import Signature, signature
from types import FunctionType
from typing import Any, Callable, List

class FunctionMetadata:
    name: str
    signature: Signature

    def __init__(self, fn: Callable):
        assert type(fn) == FunctionType, "fn should be a function"
        self.signature = signature(fn)
        self.name = fn.__name__

class PydanticSchemaBuilder:
    def __init__(self):
        self.funcs: List[FunctionMetadata] = []

builder = PydanticSchemaBuilder()

def plow(fn: Callable):
    builder.funcs.append(FunctionMetadata(fn))
    return fn

StepSchema = Any ## TODO: Generate NodeType Union

class PlowSchema:
    name: str
    inputs: Any
    steps: List[StepSchema]
    

