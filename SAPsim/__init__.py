__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from pathlib import Path
from typing import Any
from SAPsim.utils.parser import parse_csv
import SAPsim.utils.helpers as helpers
import SAPsim.utils.globs as globs
import SAPsim.utils.execute as execute


def run(prog_path: str, **kwargs) -> None:
    r"""Run given .csv program.

    :param prog_path:
        .csv file in SAPsim format.
    :type prog_path: ``str``
    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *debug* (``bool``) --
            * Whether to run in debug mode (True) or at full speed (False)
            * Default is full speed
        * *change* (``str``) --
            * Comma-separated list of changes to RAM
            * Useful for debugging programs (edit a value without changing CSV)
            * Also useful for autograding programs (overwrite a reserved instruction/data value)
            * Format: <addr>:<base-10 value>,<addr>:<base-10 value>, ...
        * *format* (``str``) --
            * Table format
            * Options: https://github.com/astanin/python-tabulate#table-format
        * *bits* (``int``) --
            * Number of bits in unsigned registers
            * Default 8
    :return: ``dict`` containing all final values in globs.py, used for autograding
    :rtype: ``dict``
    """
    path: Path = Path(prog_path)
    assert path.suffix == ".csv"
    helpers.setup_8bit()
    parse_csv(path)
    if "bits" in kwargs:
        assert int(kwargs["bits"]) > 1
        globs.NUM_BITS_IN_REGISTERS = int(kwargs["bits"])
        globs.MAX_UNSIGNED_VAL_IN_REGISTERS = 2**globs.NUM_BITS_IN_REGISTERS - 1
    if "change" in kwargs:
        changes = kwargs["change"].split(",")
        for change in changes:
            if change.count(":") != 1:
                print(
                    "Invalid syntax for --c option, correct format is <addr>:<base-10 value>,<addr>:<base-10 value>, ..."
                )
                exit(1)
            colon_position = change.find(":")
            addr = int(change[:colon_position])
            if addr not in globs.RAM:
                print(
                    f"You can apply a change only to an address that's already mapped (not skipped). Address {addr} is not mapped."
                )
                exit(1)
            value = int(change[colon_position + 1 :])
            if value < 0 or value > globs.MAX_UNSIGNED_VAL_IN_REGISTERS:
                print(
                    f"Invalid base-10 value for change: {value}. Negative or overflows registers."
                )
                exit(1)
            globs.RAM[addr] = value
    if "format" in kwargs:
        globs.table_fmt = kwargs["format"]
    if "debug" in kwargs and kwargs["debug"]:
        print("Initial state of simulation.")
        helpers.print_RAM(dispPC=True)
        helpers.print_info()
        print("Debug mode: press Enter to execute next instruction ( > ).")
        input()
        while globs.EXECUTING:
            # Special case so that you don't have to press Enter twice to halt on a HLT instruction
            if (
                globs.PC in globs.RAM
                and helpers.parse_opcode(globs.RAM[globs.PC]) == 0xF
            ):
                execute.execute_next()
                break
            execute.execute_next()
            helpers.print_RAM(dispPC=True)
            helpers.print_info()
            input()
        print("Program halted.")
    else:
        execute.execute_full_speed()
        helpers.print_RAM(dispPC=True)
        helpers.print_info()
        print("Program halted.")


def run_and_return_state(prog_path: str, **kwargs) -> dict[str, Any]:
    r"""Run given .csv program and return final state. Just a wrapper around ``run()`` that can be used for autograding.

    The rest of the docstring is identical to that of run().

    :param prog_path:
        .csv file in SAPsim format.
    :type prog_path: ``str``
    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *debug* (``bool``) --
            * Whether to run in debug mode (True) or at full speed (False)
        * *change* (``str``) --
            * Comma-separated list of changes to RAM
            * Useful for debugging programs (edit a value without changing CSV)
            * Also useful for autograding programs (overwrite a reserved instruction/data value)
            * Format: <addr>:<base-10 value>,<addr>:<base-10 value>, ...
        * *format* (``str``) --
            * Table format
            * Options: https://github.com/astanin/python-tabulate#table-format
        * *bits* (``int``) --
            * Number of bits in unsigned registers
    :return: ``dict`` containing all final values in globs.py, used for autograding
    :rtype: ``dict``
    """
    run(prog_path, **kwargs)
    return helpers.get_state()
