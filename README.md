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

- [ ] Basic execution of DAGs

  1. Implement a decorator to register functions as building blocks for workflows
  2. Create a workflow assembler, that takes a YAML file describing the workflow,
     collects the used functions, and iterate through the defined tasks in topological
     order

  The following python libs/functions will help us do that:

  - [pydantic](https://pydantic-docs.helpmanual.io/)
    - Validating the workflow YAMLs
  - [inspect](https://docs.python.org/3/library/inspect.html)
    - Get python functions signature at runtime
  - [graphlib](https://docs.python.org/3/library/graphlib.html)
    - Validation of the workflow DAG
    - Topological iteration of tasks
  - [eval](https://docs.python.org/3/library/functions.html#eval)
    -  Evalute the reference strings, e.g. "$inputs.x"

- [ ] Editor support
  1. Enable autocompletion from a JSON Schema produced by a pydantic
     model generated through inspecting the internals of collected tasks
  2. Improve the default JSON schema completion to use the workflow context as completion source
  
  
# Similar
- [Airflow](https://github.com/apache/airflow)
