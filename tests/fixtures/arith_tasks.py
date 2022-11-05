import plow


def quadratic_solver_tasks():
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
