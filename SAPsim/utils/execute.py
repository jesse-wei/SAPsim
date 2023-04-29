"""Execute instructions in RAM."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from pathlib import Path
from typing import Any
import SAPsim.utils.global_vars as global_vars
import SAPsim.utils.instructions as instructions
import SAPsim.utils.helpers as helpers
from SAPsim.utils.helpers import is_documented_by
import SAPsim.utils.exceptions as exceptions
import SAPsim.utils.parser as parser


def execute_full_speed() -> None:
    """Execute instructions in ``RAM`` at full speed until ``EXECUTING`` is ``False`` or ``PC > max addr``."""
    max_addr: int = 0
    if global_vars.RAM.keys():
        max_addr = max(global_vars.RAM.keys())
    while global_vars.EXECUTING:
        # Check that RAM is non-empty.
        if global_vars.RAM.keys() and global_vars.PC > max_addr:
            global_vars.EXECUTING = False
            raise exceptions.DroppedOffBottom

        # If we're executing an empty address but it's not a DroppedOffBottom, just skip and don't execute
        if global_vars.PC not in global_vars.RAM:
            global_vars.PC += 1
            continue

        instructions.OPCODE_TO_INSTR_PROCEDURE[
            helpers.parse_opcode(global_vars.RAM[global_vars.PC])
        ](helpers.parse_arg(global_vars.RAM[global_vars.PC]))


def execute_next() -> None:
    """Execute a single instruction at the current ``PC`` value if ``EXECUTING``. If attempting to execute an empty address, ``PC += 1`` (i.e., doesn't skip to next filled address)."""
    if global_vars.EXECUTING:
        if global_vars.RAM.keys() and global_vars.PC > max(global_vars.RAM.keys()):
            global_vars.EXECUTING = False
            raise exceptions.DroppedOffBottom

        # If executing an empty address, just skip and don't execute
        if global_vars.PC not in global_vars.RAM:
            global_vars.PC += 1
        else:
            instructions.OPCODE_TO_INSTR_PROCEDURE[
                helpers.parse_opcode(global_vars.RAM[global_vars.PC])
            ](helpers.parse_arg(global_vars.RAM[global_vars.PC]))


def run(prog_path: str, **kwargs) -> None:
    r"""Run given .csv program in SAPsim format.

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
            * Format: <addr>:<base-10 value>,<addr>:<base-10 value>,...
            * The value at each address will be overwritten to that base-10 value
            * Useful for debugging programs (edit a value without changing CSV)
            * Also useful for autograding programs (overwrite a reserved instruction/data value)
        * *table_format* (``str``) --
            * Table format
            * Options: https://github.com/astanin/python-tabulate#table-format
            * Default value is "simple_outline"
        * *bits* (``int``) --
            * Number of bits in unsigned registers
            * Default 8
    :return: ``None``
    """
    if not isinstance(prog_path, str):
        raise TypeError("Required parameter prog_path must be a str.")
    if "debug" in kwargs and not isinstance(kwargs["debug"], bool):
        raise TypeError("Keyword argument debug must be a bool.")
    if "change" in kwargs and not isinstance(kwargs["change"], str):
        raise TypeError("Keyword argument change must be a str.")
    if "table_format" in kwargs and not isinstance(kwargs["table_format"], str):
        raise TypeError("Keyword argument table_format must be a str.")
    if "bits" in kwargs and not isinstance(kwargs["bits"], int):
        raise TypeError("Keyword argument bits must be an int.")

    path: Path = Path(prog_path)
    if not path.suffix == ".csv":
        raise exceptions.FileNotCSV(path)
    helpers.setup_8bit()
    parser.parse_csv(path)
    if "bits" in kwargs:
        assert kwargs["bits"] > 1
        global_vars.NUM_BITS_IN_REGISTERS = kwargs["bits"]
    if "change" in kwargs:
        changes = kwargs["change"].split(",")
        for change in changes:
            if change.count(":") != 1:
                print(
                    "Invalid syntax for change parameter, correct format is <addr>:<base-10 value>, <addr>:<base-10 value>, ..."
                )
                exit(1)
            change = change.strip()
            colon_position = change.find(":")
            addr = int(change[:colon_position])
            if addr not in global_vars.RAM:
                print(
                    f"You can apply a change only to an address that's already mapped (not skipped). Address {addr} is not mapped."
                )
                exit(1)
            value = int(change[colon_position + 1 :])
            if value < 0 or value > (2**global_vars.NUM_BITS_IN_REGISTERS - 1):
                print(
                    f"Invalid base-10 value for change: {value}. Negative or overflows registers."
                )
                exit(1)
            global_vars.RAM[addr] = value
    if "table_format" in kwargs:
        global_vars.table_format = kwargs["table_format"]
    if "debug" in kwargs and kwargs["debug"]:
        print(f"Initial state of simulation of {prog_path}")
        helpers.print_RAM(dispPC=True)
        helpers.print_info()
        print("Debug mode: press Enter to execute next instruction ( > ).")
        input()
        while global_vars.EXECUTING:
            # Special case so that you don't have to press Enter twice to halt on a HLT instruction
            if (
                global_vars.PC in global_vars.RAM
                and helpers.parse_opcode(global_vars.RAM[global_vars.PC]) == 0xF
            ):
                execute_next()
                break
            execute_next()
            helpers.print_RAM(dispPC=True)
            helpers.print_info()
            input()
        print("Program halted.")
    else:
        execute_full_speed()
        helpers.print_RAM(dispPC=True)
        helpers.print_info()
        print("Program halted.")


@is_documented_by(
    run,
    2,
    "",
    r"""
    :return: ``dict`` containing program state (see ``helpers.get_state``)
    :rtype: ``dict[str, Any]``
    """,
)
def run_and_return_state(prog_path: str, **kwargs) -> dict[str, Any]:
    run(prog_path, **kwargs)
    return helpers.get_state()
