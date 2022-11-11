import re
import yaml
import graphlib
from pathlib import Path
from typing import Any, Callable, List, Optional, Type, Union
from pydantic import BaseModel
from plow import schema_gen
from plow.decorators import clean_builder, get_func
from plow.utils import import_plow_decorated_funcs

ref_regex = re.compile(r"(\$[\w\.]+|\${[^}]*})")


class StepSchema(BaseModel):
    alias: str
    type: str
    args: Any
    depends: Optional[List[str]] = None


class Dag(BaseModel):
    class Config:
        underscore_attrs_are_private = True

    name: Optional[str]
    description: Optional[str]
    inputs: Any
    steps: List[StepSchema]
    _mem: dict[str, Any]
    _steps_by_alias: dict[str, StepSchema] = {}
    _stopped: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._steps_by_alias = {step.alias: step for step in self.steps}
        self._mem = {}
        if self.inputs:
            self.save_inputs(self.inputs)
        self._stopped = False

    def save_inputs(self, inputs: dict[str, Any]):
        self._mem["inputs"] = {}
        for key, v in inputs.items():
            self._mem["inputs"][key] = v

    def _read(self, key: Any) -> Any:
        if isinstance(key, str):
            if self._is_reference(key):
                refs = self._unwrap_dollar(key)
                assert len(refs) == 1, "Only read one at a time"
                ref = refs[0]
                splitted_ref = ref.split(".")
                ref_key = splitted_ref[0]
                ref_attributes = splitted_ref[1:]
                from_mem = self._mem[ref_key]
                value = from_mem
                for attribute in ref_attributes:
                    try:
                        # Try accessing as attribute
                        value = getattr(value, attribute)
                    except AttributeError:
                        # Try accessing as dict
                        value = value[attribute]

                return value
        return key

    def _process(self, step: StepSchema):
        func = get_func(func_name=step.type)
        callable = func.ref()
        if step.depends:
            for depend in step.depends:
                references = self._unwrap_dollar(depend)
                references_values = {ref: self._read(f"${ref}") for ref in references}
                step_evaluated = depend
                for ref, val in references_values.items():
                    val = str(val)
                    step_evaluated = re.compile(rf"\${ref}").sub(val, step_evaluated)
                    step_evaluated = re.compile(r"\${" + ref + "}").sub(
                        val, step_evaluated
                    )
                globals = {"return_": None}
                try:
                    exec(f"return_ = {step_evaluated}", globals)
                except SyntaxError:
                    raise SyntaxError(f"Could not evaluate {step_evaluated}")
                if not globals["return_"]:
                    self._stopped = True
                    return

        if isinstance(step.args, dict):
            args = {
                arg_name: self._read(arg_value)
                for arg_name, arg_value in step.args.items()
            }
            args = step.Args.parse_obj(args)  # noqa
            args = {
                arg_name: getattr(args, arg_name) for arg_name in args.__fields__.keys()
            }
            self._mem[step.alias] = callable(**args)
        elif isinstance(step.args, list):
            raise Exception("not anymore")
            args = [self._read(arg_value) for arg_value in step.args]
            self._mem[step.alias] = callable(*args)
        else:
            raise TypeError("step args must be dict or list")

    def run(self, inputs: Optional[dict[str, Any]] = None) -> Any:
        if inputs:
            self._mem = {}
            self.save_inputs(inputs)
        self.iterate_toposort(lambda s: self._process(s))
        return self._mem  # TODO: return more meaningful output

    @staticmethod
    def _is_input(value: str) -> bool:
        return value.startswith("inputs.")

    @staticmethod
    def _is_reference(value: str) -> bool:
        return value.startswith("$")

    @staticmethod
    def _unwrap_dollar(value: str) -> list[str]:
        """
        Takes a string and returns

        """
        if isinstance(value, str):
            iterator = ref_regex.finditer(value)
            if not ref_regex.search(value):
                raise Exception("No reference in value")
            result = []
            for match in iterator:
                match_str = value[match.start() : match.end()]
                if match_str.startswith("${") and match_str.endswith("}"):
                    start = match.start() + 2
                    end = match.end() - 1
                    result.append(value[start:end])
                elif match_str.startswith("$"):
                    start = match.start() + 1
                    end = match.end()
                    result.append(value[start:end])
            return result

    def _get_outgoing_steps(self, step_name) -> list[str]:
        step = self._steps_by_alias[step_name]
        arg_values = step.args.values() if isinstance(step.args, dict) else step.args
        refs: list[str] = []
        for value in arg_values:
            if not isinstance(value, str):
                continue
            if self._is_reference(value) and not self._is_input(value):
                for ref in self._unwrap_dollar(value):
                    first_ref = ref.split(".")[0]
                    refs.append(first_ref)
        if step.depends:
            for depend in step.depends:
                for ref in self._unwrap_dollar(depend):
                    refs.append(ref)
        return refs

    def iterate_toposort(self, fn: Callable[[StepSchema], None]):
        sorter = graphlib.TopologicalSorter()

        for step in self.steps:
            outgoing = self._get_outgoing_steps(step.alias)
            sorter.add(step.alias, *outgoing)
        nodes = sorter.static_order()
        for node in nodes:
            if node not in self._steps_by_alias:
                continue
            step = self._steps_by_alias[node]
            fn(step)
            if self._stopped:
                break


def make_dag(
    *,
    yaml_path: Optional[Union[Path, str]] = None,
    yaml_str: Optional[str] = None,
) -> Dag:
    assert yaml_str or yaml_path, "yaml_str or yaml_path is required"
    yaml_values = {}
    if yaml_str:
        yaml_values = yaml.unsafe_load(yaml_str)
    elif yaml_path:
        with open(yaml_path, "rb") as f:
            yaml_values = yaml.unsafe_load(f)

    return Dag(**yaml_values)


def make_improved_dag_class(src_module: Optional[str]) -> Type[Dag]:
    if src_module:
        clean_builder()  # makes sure builder is in a clean state
        import_plow_decorated_funcs(src_module)
    script = schema_gen.generate_schemas_script()  # gen script defining Step
    exec(script, globals())  # Run script

    class DagOverwritten(Dag):  # overite Dag schema with generated steps
        steps: List[Step]  # noqa

    return DagOverwritten


def make_improved_dag(
    *,
    yaml_path: Optional[Union[Path, str]] = None,
    yaml_str: Optional[str] = None,
    src_module: Optional[str] = None,
) -> Dag:
    BetterDag = make_improved_dag_class(src_module)
    assert yaml_str or yaml_path, "yaml_str or yaml_path is required"
    if yaml_str:
        yaml_values = yaml.unsafe_load(yaml_str)
    elif yaml_path:
        with open(yaml_path, "rb") as f:
            yaml_values = yaml.unsafe_load(f)
    else:
        raise Exception(
            f"yaml_str or yaml_path must be strings, got {yaml_str} and {yaml_path}"
        )
    return BetterDag(**yaml_values)
