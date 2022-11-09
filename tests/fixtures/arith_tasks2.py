from pydantic import BaseModel
import plow


class Foo(BaseModel):
    attr: int


class Bar(BaseModel):
    attr2: int


def define_tasks():
    @plow.task
    def add_(a: int, b: int):
        return a + b

    @plow.task
    def add(a: Foo, b: Bar):
        return a.attr + b.attr2
