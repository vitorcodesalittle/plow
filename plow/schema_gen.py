"""
This package have functions generate to pydantic schemas for functions
decorated with plow.task
"""
import sys

import ast
from plow.decorators import clean_builder, get_all_funcs, FunctionMetadata
from inspect import Parameter
from typing import List, Optional

from plow.utils import import_plow_decorated_funcs


def strip_class(class_str: str):
    if class_str.startswith("<class '") and class_str.endswith("'>"):
        return class_str[8:-2]
    return class_str


def gen_step_and_args(
    function_metadata: FunctionMetadata,
) -> tuple[ast.ClassDef, List[str]]:
    fn_name = function_metadata.name
    args_class_name = "Args"
    step_class_name = f"{fn_name}_step"
    step_class_body = [
        ast.AnnAssign(
            target=ast.Name(id="type", ctx=ast.Store()),
            annotation=ast.Name(id=f'Literal["{fn_name}"]', ctx=ast.Load()),
            value=ast.Constant(value=fn_name),
            simple=1,
        ),
        ast.AnnAssign(
            target=ast.Name(id="alias", ctx=ast.Store()),
            annotation=ast.Name(id="str", ctx=ast.Load()),
            simple=1,
        ),
        ast.AnnAssign(
            target=ast.Name(id="args", ctx=ast.Store()),
            annotation=ast.Name(id=f"List[str] | Dict[str, Any]", ctx=ast.Load()),
            simple=1,
        ),
        ast.AnnAssign(
            target=ast.Name(id="depends", ctx=ast.Store()),
            value=ast.Constant(None),
            annotation=ast.Name(id=f"Optional[List[str]]", ctx=ast.Load()),
            simple=1,
        ),
    ]
    args_class_body: List[ast.AST] = []
    imports = []
    for key, value in function_metadata.signature.parameters.items():
        assert (
            value.annotation != Parameter.empty
        ), "function parameters should have annotation"
        if value.default == Parameter.empty:
            ann = strip_class(str(value.annotation))
            parts = ann.split(".")
            if len(parts) > 1:
                imports.append(".".join(parts))
                ann = parts[-1]
            args_class_body.append(
                ast.AnnAssign(
                    target=ast.Name(id=key, ctx=ast.Store()),
                    annotation=ast.Name(id=ann),
                    simple=1,
                )
            )
        else:
            raise Exception("Not implemented")

    args_ast = ast.ClassDef(
        name=args_class_name,
        bases=[ast.Name(id="BaseModel", ctx=ast.Load())],
        keywords=[],
        body=args_class_body,
        decorator_list=[],
    )

    step_ast = ast.ClassDef(
        name=step_class_name,
        bases=[ast.Name(id="BaseModel", ctx=ast.Load())],
        keywords=[],
        body=step_class_body + [args_ast],
        decorator_list=[],
    )

    return step_ast, imports


def gen_module():
    script_defs: List[ast.AST] = []
    step_names: List[str] = []
    imports = []
    for func in get_all_funcs():
        step, imports_ = gen_step_and_args(func)
        script_defs += [step]
        step_names.append(step.name)
        imports += imports_
    imports = list(set(imports))
    m = ast.Module(
        body=[
            ast.ImportFrom(
                module=".".join(import_.split(".")[:-1]),
                names=[ast.alias(name=import_.split(".")[-1])],
                level=0,
            )
            for import_ in imports
        ]
        + [
            ast.ImportFrom(
                module="typing",
                names=[
                    ast.alias(name="Union"),
                    ast.alias(name="Literal"),
                    ast.alias(name="Any"),
                    ast.alias(name="Dict"),
                ],
                level=0,
            ),
            ast.ImportFrom(
                module="pydantic.main", names=[ast.alias(name="BaseModel")], level=0
            ),
        ]
        + script_defs
        + [
            ast.Assign(
                targets=[ast.Name(id="Step", ctx=ast.Store())],
                value=ast.Subscript(
                    value=ast.Name(id="Union", ctx=ast.Load()),
                    slice=ast.Tuple(
                        elts=[
                            ast.Name(id=step_name, ctx=ast.Load())
                            for step_name in step_names
                        ],
                        ctx=ast.Load(),
                    ),
                    ctx=ast.Load(),
                ),
            ),
        ],
        type_ignores=[],
    )
    return m


def generate_schemas_script(src_module: Optional[str] = None):
    if src_module:
        # makes sure builder is in a clean state
        clean_builder()
        # import decorated functions
        import_plow_decorated_funcs(src_module)
    # gen script defining Step
    script = gen_module()
    script = ast.fix_missing_locations(script)
    return ast.unparse(script)


if __name__ == "__main__":
    print(generate_schemas_script(sys.argv[1] or None))
