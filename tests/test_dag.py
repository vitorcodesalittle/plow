import pytest

import plow
from plow.dag import Dag


class TestDag:
    @pytest.fixture(scope="function")
    def dag_fixture(self, quadratic_solver_yaml_fixture: str) -> Dag:
        return plow.make_dag(yaml_str=quadratic_solver_yaml_fixture)

    def test_unwrap_dollar(self):
        assert Dag._unwrap_dollar("$inputs") == ["inputs"]
        assert Dag._unwrap_dollar("$inputs.a.b.c $other.a.b.c") == [
            "inputs.a.b.c",
            "other.a.b.c",
        ]
        assert Dag._unwrap_dollar(
            "${other_layer.x} ${don't recommend this but should work}"
        ) == ["other_layer.x", "don't recommend this but should work"]

    def test_get_outgoing_steps(self, dag_fixture: Dag):
        assert dag_fixture._get_outgoing_steps("sqrt_disc") == ["disc"]
        assert dag_fixture._get_outgoing_steps("positive_num") == [
            "minus_b",
            "sqrt_disc",
        ]
