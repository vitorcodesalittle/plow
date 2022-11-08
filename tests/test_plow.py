import plow
from plow.dag import Dag


def test_dag(quadratic_solver_tasks_fixture: None, quadratic_solver_yaml_fixture: str):
    dag = plow.make_dag(yaml_str=quadratic_solver_yaml_fixture)
    assert isinstance(dag, Dag), "make_dag fails to create Dag with valid yaml"
    result = dict(dag.run(inputs={"a": -4, "b": 2, "c": 6}))
    assert result["root_1"] == -1
    assert result["root_2"] == 1.5


def test_dag_with_control_flow(
    quadratic_solver_tasks_fixture: None, quadratic_solver_cf_yaml_fixture: str
):
    dag = plow.make_dag(yaml_str=quadratic_solver_cf_yaml_fixture)
    result = dict(dag.run({"a": 2, "b": 4, "c": 2}))
    assert "disc" in result
    assert "sqrt_disc" not in result
