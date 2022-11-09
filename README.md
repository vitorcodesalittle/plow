# Plow

Plow is a python package for building and running DAG workflows,
described by yaml files and powered by your own python functions.

## Goals

- [x] Basic execution of DAGs

  1. Implement a decorator to register functions as building blocks for workflows
  2. Create a workflow assembler, that takes a YAML file describing the workflow,
     collects the used functions, and iterate through the defined tasks in topological
     order

- [x] Advanced execution of workflows:

  1. Support control flow, i.e. provide mechanisms for if_else conditions, and not necessarily execute the whole DAG [here are some ideas](./CONTROL_FLOW_IDEAS.md)

- [x] [Basic Editor support](./plow/json_schema.py)

  1. Enable autocompletion from a JSON Schema produced by a pydantic
     model generated through inspecting the internals of collected tasks

- [ ] Advanced Editor support 2. Improve the default JSON schema completion to use the workflow context as completion source,
      e.g. when pressing `$` when filling a `args` get's all `alias` and `input` as options for completion. Even better, only those that
      actually match the type signature.

- [ ] Documentation, publishing and CI
  1. [ ] Document Dag schema attribute
  2. [ ] Pydocs on exported functions
  3. [ ] sphinx
  4. [ ] CI: lint -> test -> gen docs -> publish in pip -> update sphinx github page

# Similar

- [Airflow](https://github.com/apache/airflow)
