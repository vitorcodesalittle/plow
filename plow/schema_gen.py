"""
This package have functions to create narrow schemas for the pydantic steps
"""

import ast
from plow.decorators import get_all_funcs, FunctionMetadata
from inspect import Parameter
from typing import List

from tests.conftest import quadratic_solver_tasks


def gen_step_and_args(
    function_metadata: FunctionMetadata,
) -> tuple[ast.ClassDef, ast.ClassDef]:
    fn_name = function_metadata.name
    args_class_name = f"{fn_name}_args"
    step_class_name = f"{fn_name}_step"
    step_class_body = [
        ast.AnnAssign(
            target=ast.Name(id="alias", ctx=ast.Store()),
            annotation=ast.Name(id="str", ctx=ast.Load()),
            simple=1,
        ),
        ast.Assign(
            targets=[ast.Name(id="type", ctx=ast.Store())],
            value=ast.Constant(value=fn_name),
        ),
        ast.AnnAssign(
            target=ast.Name(id="args", ctx=ast.Store()),
            annotation=ast.Name(id=args_class_name, ctx=ast.Load()),
            simple=1,
        ),
    ]
    args_class_body: List[ast.AST] = []
    for key, value in function_metadata.signature.parameters.items():
        assert (
            value.annotation != Parameter.empty
        ), "function parameters should have annotation"
        if value.default == Parameter.empty:
            args_class_body.append(
                ast.AnnAssign(
                    target=ast.Name(id=key, ctx=ast.Store()),
                    annotation=ast.Name(id=value.annotation),
                    simple=1,
                )
            )
        else:
            ...

    step_ast = ast.ClassDef(
        name=step_class_name,
        bases=[ast.Name(id="BaseModel", ctx=ast.Load())],
        keywords=[],
        body=step_class_body,
        decorator_list=[],
    )
    args_ast = ast.ClassDef(
        name=args_class_name,
        bases=[ast.Name(id="BaseModel", ctx=ast.Load())],
        keywords=[],
        body=args_class_body,
        decorator_list=[],
    )
    return step_ast, args_ast


def gen_module():
    script_defs: List[ast.AST] = []
    step_names: List[str] = []
    for func in get_all_funcs():
        step, args = gen_step_and_args(func)
        script_defs += [step, args]
        step_names.append(step.name)
    m = ast.Module(
        body=[
            ast.ImportFrom(module="typing", names=[ast.alias(name="Union")], level=0),
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


quadratic_solver_tasks()  # import decorated functions
script = gen_module()
script = ast.fix_missing_locations(script)
print(ast.unparse(script))
