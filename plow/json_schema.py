"""
This package provides access to the json schema of decorated functions

Types of access implemented:
1. stdout

Wanted types of acecss:
2. as a web server that updates on source changes
"""

from plow.dag import make_improved_dag_class


def add_lines(multiline: str):
    return "\n".join(
        [f"{idx + 1:2d} {line}" for idx, line in enumerate(multiline.split("\n"))]
    )


def print_schema(src_module: str):
    """
    Print JSON schema using plow.task decorated functions
    in `src_module`"""
    BetterDag = make_improved_dag_class(src_module=src_module)
    print(BetterDag.schema_json(indent=2))


if __name__ == "__main__":
    import sys

    src_module = sys.argv[1]
    print_schema(src_module)
