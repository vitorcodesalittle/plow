import plow
from plow.dag import Dag

def test_dag(quadratic_solver_tasks:None, quadratic_solver_yaml_fixture: str):
    dag = plow.make_dag(yaml_str=quadratic_solver_yaml_fixture)
    assert isinstance(dag, Dag), "make_dag failes to create Dag with valid yaml"
    result = dict(dag.run(inputs={'a': -4, 'b': 2, 'c': 6}))
    assert result['root_1'] == -1
    assert result["root_2"] == 1.5

