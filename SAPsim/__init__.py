__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from typing import Union, Any
from SAPsim.utils.helpers import is_documented_by
from SAPsim.utils.global_vars import MAX_PC
import SAPsim.utils.execute as execute


# Weird glitch, passing in the function doesn't actually get its docstring? Just append then
@is_documented_by(execute.run, 0, "", execute.run.__doc__)
def run(prog_path: str, **kwargs) -> Union[None, dict[str, Any]]:
    return execute.run(prog_path, **kwargs)


def create_template(path: str = "template.csv") -> None:
    r"""
    Create blank template file in SAPsim format in current directory.

    :param path: Path to create template file at. Defaults to ``template.csv``.
    :type path: str
    :return: None
    """
    # This will rarely be used so doesn't need to be imported at top level
    import csv

    header: list[str] = ["Address", "First Hexit", "Second Hexit", "Comments"]
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(MAX_PC):
            writer.writerow([f"{i}", "", "", ""])
    print(f"{path} successfully created.")
