# Plow

Plow is a python package for quickly building workflows based on python defined tasks.
Workflows are represented as Directed Acyclic Graphs (DAG), and specified through a yaml
file. A JSON schema is generated based on the tasks defined, and is useful while typing the
yaml files.

## Goals

- [x] Execution of workflows:
- [x] [Basic editor support](./plow/json_schema.py)
- [ ] Advanced editor support. Improve the default JSON schema completion to use the workflow context as completion source,
      e.g. when pressing `$` when filling a `args` get's all `alias` and `input` as options for completion. Even better, only those that
      actually match the type signature.

# Similar

- [Airflow](https://github.com/apache/airflow)
