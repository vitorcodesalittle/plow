import pytest
from pydantic.main import BaseModel
from pydantic.networks import EmailStr
import plow
from plow.dag import Dag


def test_dag(quadratic_solver_tasks_fixture: None, quadratic_solver_yaml_fixture: str):
    dag = plow.make_improved_dag(yaml_str=quadratic_solver_yaml_fixture)
    assert isinstance(dag, Dag), "make_dag fails to create Dag with valid yaml"
    result = dict(dag.run(inputs={"a": -4.0, "b": 2.0, "c": 6.0}))
    assert result["root_1"] == -1
    assert result["root_2"] == 1.5


def test_dag_with_control_flow(
    quadratic_solver_tasks_fixture: None, quadratic_solver_cf_yaml_fixture: str
):
    dag = plow.make_improved_dag(yaml_str=quadratic_solver_cf_yaml_fixture)
    result = dict(dag.run({"a": 2, "b": 4, "c": 2}))
    assert "disc" in result
    assert "sqrt_disc" not in result


@pytest.mark.parametrize(
    "yaml_str",
    [
        """
name: test
description: ...
inputs:
  a:
    attr: 3
  b:
    attr2: 4
steps:
  - alias: sum
    type: add
    args:
      a: $inputs.a
      b: $inputs.b
    """,
        """
name: test
description: ...
inputs:
  a:
    attr: 3
  b:
    attr2: 4
steps:
  - alias: sum
    type: add_
    args:
      a: $inputs.a.attr
      b: $inputs.b.attr2
    """,
    ],
)
def test_dag_with_pydantic_tasks(yaml_str: str, arith_tasks2_fixture):
    dag = plow.make_improved_dag(yaml_str=yaml_str)
    result = dict(dag.run())
    assert result["sum"] == 7
