# Plow 🌹🔫

Plow is a python package for quickly building workflows based on python functions as tasks.
Workflows are represented as directed acyclic graphs, and specified through a yaml file.
A JSON schema is generated based on the tasks defined, and together with [yamlls](https://github.com/redhat-developer/yaml-language-server)
is useful to provide completion when typing the yaml file.

> This project has not been battle tested, and ~~probably~~ has bugs. If you find it interesting, please try it and let me know
> of bugs/questions/ideas.

## Quickstart

Defining what workflows can do might be easy coming from python functions.
For plow to run properly, the task functions have some requirements:
- Parameters must have type hints, and be either primitives (float, int, str, bool) or [pydantic BaseModel](https://pydantic-docs.helpmanual.io/usage/models/).
- Only positional parameters (this will soon be relaxed to allow keyword argument)

```python
import plow

@plow.task
def add(a: float, b: float) -> float:
    return a + b
```

Once this is done, use the script as `--tasks_path` for the commands below so plow knows where to find the task definitions.

## Brief YAML Spec

```
name: ArithmeticExampleWithControlFlow         # Name of the workflow (not used)
description: executes (-b +- sqrt(b²-4ac))/2a  # Description of the wk (not used)
steps:                                         # Starts defining the DAG
  - alias: 4ac                                 # Node name
    type: multiply                             # Python step function
    args:                                      # step function args
      a: 4                                     # -- an arg may be a value ...
      b: $ac                                   # -- or a reference to other step's output
    deoends:                                   # -- Add predicates that may turn this branch off
      - $other_step.result > 0
```

## Commands

- `python -m plow.main print --tasks_path <path to python module/script where steps are defined>`: Prints the json schema to stdout.
- `python -m plow.main run --tasks_path ... <path to workflow yaml>`: Runs a workflow, and outputs the resulting python dict. Each entry is a step's output

## Securiy

Running workflows with user input is not safe as plow doesn't sanitize what's passed to some `exec` calls, and might lead to Remote Code Execution.

## Goals

- [x] Execution of workflows:
- [x] [Basic editor support](./plow/json_schema.py)
- [ ] Advanced editor support. Improve the default JSON schema completion to use the workflow context as completion source,
      e.g. when pressing `$` when filling an `args` get's all `alias` and `input` as options for completion. Even better, only those that
      actually match the type signature.
- [ ] Make it safe to use with untrusted input

# Similar

- [Airflow](https://github.com/apache/airflow): More robust alternative for running workflows
