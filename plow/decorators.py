from inspect import Signature, signature
from types import FunctionType
from typing import Callable, List

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

    def clean(self):
        self.funcs = []

builder = PydanticSchemaBuilder()

def clean_builder():
    builder.clean()

def task(fn: Callable):
    builder.funcs.append(FunctionMetadata(fn))
    return fn

