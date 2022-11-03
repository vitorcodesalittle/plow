"""
This package provides access to the json schema of decorated functions

Types of access implemented:
1. stdout

Wanted types of acecss:
2. as a web server that updates on source changes
"""

from typing import List
from plow import schema_gen
from plow.dag import Dag
from plow.decorators import clean_builder


def add_lines(multiline: str):
    return "\n".join(
        [f"{idx + 1:2d} {line}" for idx, line in enumerate(multiline.split("\n"))]
    )


def print_schema(src_module: str, debug=False):
    """
    Print JSON schema using plow.task decorated functions
    in `src_module`"""
    clean_builder()  # makes sure builder is in a clean state
    __import__(src_module)  # import decorated functions
    script = schema_gen.generate_schemas_script()  # gen script defining Step
    if debug:
        print(add_lines(script))

    exec(script, globals())  # Run script

    class DagOverwritten(Dag):  # overite Dag schema with generated steps
        steps: List[Step]  # noqa

    print(DagOverwritten.schema_json(indent=2))


if __name__ == "__main__":
    import sys

    src_module = sys.argv[1]
    print_schema(src_module)
