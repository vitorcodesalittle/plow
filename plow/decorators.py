from inspect import Signature, signature
from types import FunctionType
from typing import Callable, List, Any


class FunctionMetadata:
    name: str
    signature: Signature
    _ref: Any = None

    def __init__(self, fn: Callable):
        assert type(fn) == FunctionType, "fn should be a function"
        self.signature = signature(fn)
        self.name = fn.__name__
        self._ref = fn

    def ref(self):
        return self._ref


class PydanticSchemaBuilder:
    def __init__(self):
        self.funcs: List[FunctionMetadata] = []

    def clean(self):
        self.funcs = []


_builder = PydanticSchemaBuilder()


def clean_builder():
    _builder.clean()


def get_func(func_name: str) -> FunctionMetadata:
    for func in _builder.funcs:
        if func.name == func_name:
            return func
    raise ValueError(f"No func named {func_name}")


def get_all_funcs() -> List[FunctionMetadata]:
    return _builder.funcs


def task(fn: Callable):
    _builder.funcs.append(FunctionMetadata(fn))
    return fn
