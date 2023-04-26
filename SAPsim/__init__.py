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
