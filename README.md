# Plow

Plow is a python package for building and running DAG workflows,
described by yaml files and powered by your own python functions.

## Examples

- Calculates the quadratic formula

```python
# tasks.py
import plow

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
def sqrt(a: float) -> float:
  return math.sqrt(a)
```

```yaml
# quadratic.yml

name: ArithmeticExample
description: executes (-b +- sqrt(b²-4ac))/2a
inputs:
  a: -4
  b: 2
  c: 6
steps:
  - alias: ac
    type: multiply
    args:
      - $inputs.a
      - $inputs.c
  - alias: 4ac
    type: multiply
    args:
      - 4
      - $ac
  - alias: b2
    type: multiply
    args:
      a: $inputs.b
      b: $inputs.b
  - alias: disc
    type: subtract
    args:
      - $b2
      - $4ac
  - alias: sqrt_disc
    type: sqrt
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
      - sqrt_disc
  - alias: negative_num
    type: subtract
    args:
      - "$minus_b"
      - sqrt_disc
  - alias: root_1
    type: divide
    args:
      - positive_num
      - aa
  - alias: root_2
    type: divide
    args:
      - negative_sum
      - aa
```

Than the user may execute using a cli, for example:

```bash
# Runs the quadradic.yml workflow using the tasks module (tasks.py) as a source for tasks definitions
python -m plow.run --source tasks quadratic.yml
```

And check the results (the output nodes):

```
{
    "root_1": 1.5,
    "root_2": -1
}

```

## Goals

- [x] Basic execution of DAGs

  1. Implement a decorator to register functions as building blocks for workflows
  2. Create a workflow assembler, that takes a YAML file describing the workflow,
     collects the used functions, and iterate through the defined tasks in topological
     order

- [ ] Advanced execution of workflows:

  1. Support control flow, i.e. provide mechanisms for if_else conditions, and not necessarily execute the whole DAG

  - Idea 1: Built in functions

    A function implemented by us that has access to the internals of the graph during execution
    and can guide the course of execution through evaluating a predicate most probably computed from a previous step

    ```python
    def plow_if_else(predicate: bool, then_alias: str, else_alias: str) -> None:
        ...
    ```

    In the yaml files, it works the same:

    ```yaml
    - alias: Example control step
      type: plow_if_else
      args:
        - $otherstep.checked
        - proceed_onboard
        - redo_onboard
    ```

    - Idea 2: Add `depends` to step

      Depends assures one or more steps are evaluated previously

      ```yaml
      - alias: Example depends
        type: any_func
        args:
          - $used_step
        depends:
          - $other_step
      ```

      But we may also use it to turn branches off, by allowing predicates

      ```yaml
      - alias: Example depends
        type: any_func
        args:
          - $used_step
        depends:
          - $other_step.score > 5
      ```

      Using it to both control flow and arbitrary dependencies has a caveat:
      Imagine `other_step` is a function that may return False or None:

      ```yaml
      - alias: Example depends
        type: any_func
        args:
          - $used_step
        depends:
          - $other_step
      ```

      The user only wanted to add a dependency, not to control the flow, but since we're evaluating
      ` other_step`, when it returns `False` or `None`, the branch would be turned off. To ignore control flow the user will have to make the depends evaluate to `True`:

      ```yaml
      - alias: Example depends
        type: any_func
        args:
          - $used_step
        depends:
          - $other_step or True
      ```

  2. Smart ways of doing loops?

- [x] [Basic Editor support](./plow/json_schema.py)

  1. Enable autocompletion from a JSON Schema produced by a pydantic
     model generated through inspecting the internals of collected tasks

- [ ] Advanced Editor support 2. Improve the default JSON schema completion to use the workflow context as completion source,
      e.g. when pressing `$` when filling a `args` get's all `alias` and `input` as options for completion. Even better, only those that
      actually match the type signature.

  Useful links:

  - [yaml-language-server](https://github.com/redhat-developer/yaml-language-server)

- [ ] Documentation, publishing and CI

# Similar

- [Airflow](https://github.com/apache/airflow)
