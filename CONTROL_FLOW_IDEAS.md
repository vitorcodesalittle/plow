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
