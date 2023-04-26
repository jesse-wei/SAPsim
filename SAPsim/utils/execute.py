"""Execute instructions in RAM."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from pathlib import Path
from typing import Any
import SAPsim.utils.globs as globs
import SAPsim.utils.instructions as instructions
import SAPsim.utils.helpers as helpers
from SAPsim.utils.helpers import is_documented_by
import SAPsim.utils.exceptions as exceptions
import SAPsim.utils.parser as parser


def execute_full_speed() -> None:
    """Execute instructions in ``RAM`` at full speed until ``EXECUTING`` is ``False`` or ``PC > max addr``."""
    max_addr: int = 0
    if globs.RAM.keys():
        max_addr = max(globs.RAM.keys())
    while globs.EXECUTING:
        # Check that RAM is non-empty.
        if globs.RAM.keys() and globs.PC > max_addr:
            globs.EXECUTING = False
            raise exceptions.DroppedOffBottom

        # If we're executing an empty address but it's not a DroppedOffBottom, just skip and don't execute
        if globs.PC not in globs.RAM:
            globs.PC += 1
            continue

        instructions.OPCODE_TO_INSTR_PROCEDURE[
            helpers.parse_opcode(globs.RAM[globs.PC])
        ](helpers.parse_arg(globs.RAM[globs.PC]))


def execute_next() -> None:
    """Execute a single instruction at the current ``PC`` value if ``EXECUTING``. If attempting to execute an empty address, ``PC += 1`` (i.e., doesn't skip to next filled address)."""
    if globs.EXECUTING:
        if globs.RAM.keys() and globs.PC > max(globs.RAM.keys()):
            globs.EXECUTING = False
            raise exceptions.DroppedOffBottom

        # If executing an empty address, just skip and don't execute
        if globs.PC not in globs.RAM:
            globs.PC += 1
        else:
            instructions.OPCODE_TO_INSTR_PROCEDURE[
                helpers.parse_opcode(globs.RAM[globs.PC])
            ](helpers.parse_arg(globs.RAM[globs.PC]))


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
        * *table_fmt* (``str``) --
            * Table format
            * Options: https://github.com/astanin/python-tabulate#table-format
            * Default value is "simple_outline"
        * *bits* (``int``) --
            * Number of bits in unsigned registers
            * Default 8
    :return: ``None``
    """
    path: Path = Path(prog_path)
    assert path.suffix == ".csv"
    helpers.setup_8bit()
    parser.parse_csv(path)
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
            change = change.strip()
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
    if "table_fmt" in kwargs:
        globs.table_fmt = kwargs["table_fmt"]
    if "debug" in kwargs and kwargs["debug"]:
        print(f"Initial state of simulation of {prog_path}")
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
