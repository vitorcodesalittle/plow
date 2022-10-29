import pytest

from typing import Generator
import plow
from plow.decorators import clean_builder


@pytest.fixture(scope="function")
def quadratic_solver_tasks() -> Generator[None, None, None]:
    @plow.task
    def add(a: float, b: float) -> float:
        return a + b

    @plow.task
    def multiply(a: float, b: float) -> float:
        return a * b

    @plow.task
    def divide(a: float, b: float) -> float:
        return a / b

    @plow.task
    def subtract(a: float, b: float) -> float:
        return a - b

    @plow.task
    def my_sqrt(a: float) -> float:
        import math

        return math.sqrt(a)

    yield None
    clean_builder()


@pytest.fixture(scope="function")
def quadratic_solver_yaml_fixture() -> str:
    return """
name: ArithmeticExample
description: executes (-b +- sqrt(b²-4ac))/2a
inputs:
  a: -4
  b: 2
  c: 6
steps:
  - alias: 4ac
    type: multiply
    args:
      - 4
      - $ac
  - alias: root_2
    type: divide
    args:
      - $negative_sum
      - $aa
  - alias: disc
    type: subtract
    args:
      - $b2
      - $4ac
  - alias: sqrt_disc
    type: my_sqrt 
    args:
      - $disc
  - alias: minus_b
    type: multiply
    args:
      a: -1
      b: $inputs.b
  - alias: aa
    type: multiply
    args:
      - 2
      - $inputs.a
  - alias: positive_num
    type: add
    args:
      - "$minus_b"
      - $sqrt_disc
  - alias: negative_sum
    type: subtract
    args:
      - "$minus_b"
      - $sqrt_disc
  - alias: b2
    type: multiply
    args:
      a: $inputs.b
      b: $inputs.b
  - alias: ac
    type: multiply
    args:
      - $inputs.a
      - $inputs.c
  - alias: root_1
    type: divide
    args:
      - $positive_num
      - $aa
    """
