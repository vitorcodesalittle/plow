import pytest

from typing import Generator
from plow.decorators import clean_builder
from tests.fixtures.arith_tasks import quadratic_solver_tasks


@pytest.fixture(scope="function")
def quadratic_solver_tasks_fixture() -> Generator[None, None, None]:
    quadratic_solver_tasks()
    yield None
    clean_builder()


@pytest.fixture(scope="function")
def quadratic_solver_yaml_fixture():
    with open("tests/fixtures/arith.yml") as f:
        yield f.read()
