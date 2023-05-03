__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from typing import Any
from SAPsim.utils.helpers import is_documented_by
import SAPsim.utils.execute as execute


# Weird glitch, passing in the function doesn't actually get its docstring? Just append then
@is_documented_by(execute.run, 0, "", execute.run.__doc__)
def run(prog_path: str, **kwargs) -> None:
    execute.run(prog_path, **kwargs)


# Weird glitch, passing in the function doesn't actually get its docstring? Just append then
@is_documented_by(
    execute.run_and_return_state, 0, "", execute.run_and_return_state.__doc__
)
def run_and_return_state(prog_path: str, **kwargs) -> dict[str, Any]:
    return execute.run_and_return_state(prog_path, **kwargs)


def create_template() -> None:
    r"""
    Create blank ``template.csv`` file in SAPsim format in current directory.
    """
    # This will rarely be used so doesn't need to be imported at top level
    import csv

    header: list[str] = ["Address", "First Hexit", "Second Hexit", "Comments"]
    with open("template.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(16):
            writer.writerow([f"{i}", "", "", ""])
