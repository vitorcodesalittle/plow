"""
Defines CLI commands.
"""


import plow
import click
from plow.json_schema import print_schema

from plow.utils import import_plow_decorated_funcs

@click.group()
def cli():
    pass

@cli.command()
@click.option("--tasks_path", required=True, help="Path to module or script defining tasks")
@click.argument('flow_path')
def run(flow_path: str, tasks_path: str):
    """
    Runst workflow described at `flow_path` based on tasks defined in `tasks_path`
    """
    dag = plow.make_improved_dag(yaml_path=flow_path, src_module=tasks_path)
    print(dag.run())

@cli.command()
@click.option("--tasks_path", required=True, help="Path to module or script defining tasks")
def print(tasks_path: str):
    """
    Prints json schema to stdout
    """
    print_schema(tasks_path)
