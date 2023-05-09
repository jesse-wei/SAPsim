"""Execute instructions in RAM."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import sys
from pathlib import Path
from typing import Any, Union
import SAPsim.utils.global_vars as global_vars
import SAPsim.utils.instructions as instructions
import SAPsim.utils.helpers as helpers
from SAPsim.utils.helpers import is_documented_by
import SAPsim.utils.exceptions as exceptions
import SAPsim.utils.parser as parser


def execute_full_speed() -> None:
    """Execute instructions in ``RAM`` at full speed until ``EXECUTING`` is ``False`` or ``PC > max addr``.

    :return: None"""
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
    """Execute a single instruction at the current ``PC`` value if ``EXECUTING``.
    If attempting to execute an empty address, ``PC += 1`` (i.e., doesn't skip to next filled address).

    :return: None"""
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


def run(prog_path: str, **kwargs) -> Union[None, dict[str, Any]]:
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
        * *change* (``dict[int, int]``) --
            * dict[address, byte] of values to change in RAM
            * The value at each address (0 to 15) will be overwritten to that byte
            * Useful for debugging programs (edit a value without changing the CSV)
            * Useful for autograding programs (overwrite a reserved instruction/data value)
        * *table_format* (``str``) --
            * Printed table format
            * Options: https://github.com/astanin/python-tabulate#table-format
            * Default value in ``global_vars`` is ``"simple_outline"``
        * The rest of the parameters are pretty much exclusively for unit testing, and you should not use these
            * *return_state* (``bool``) --
                * If ``True``, then program state will be returned
                * See ``utils.helpers.get_state()``
                * Will probably cause type warnings since the return type is ``Union[None, dict[str, Any]]``
                * To avoid type warnings, use ``run_and_return_state``
            * *non_blocking* (``bool``) --
                * This is used to unit test debug mode of ``run()``, you likely don't have a need for this
                * If ``True``, then ``run()`` won't block on input
                * ``input()`` won't be called in debug mode (i.e., don't have to press enter to continue execution)
                * If this is ``True``, then debug mode will be on even if ``debug`` isn't in kwargs
            * *no_print* (``bool``) --
                * This is used to save computation time during unit testing
                * If ``True``, then ``print_RAM()`` and ``print_info()`` won't be called
                * In debug mode, "Program halted." will still be printed
            * *bits* (``int``) --
                * You probably don't have a need for this
                * Number of bits in registers
                * Default value in ``global_vars`` is 8
                * 8 is also the maximum value since everything in RAM should fit in a byte

    :return: ``None`` or program state if ``return_state``
    :rtype: ``Union[None, dict[str, Any]]``
    """
    if not isinstance(prog_path, str):
        raise TypeError("Required parameter prog_path must be a str.")
    debug: bool = False
    if "debug" in kwargs:
        if not isinstance(kwargs["debug"], bool):
            raise TypeError("Keyword argument debug must be a bool.")
        debug = kwargs["debug"]
    # Not initializing it causes some syntax warnings but better than initializing it
    change: dict[int, int]
    if "change" in kwargs:
        change = kwargs["change"]
        if not isinstance(change, dict):
            raise TypeError("Keyword argument change must be a dict[int, int].")
        if not all(isinstance(key, int) for key in change.keys()) or not all(
            isinstance(value, int) for value in change.values()
        ):
            raise TypeError("Keyword argument change must be a dict[int, int].")
    if "table_format" in kwargs and not isinstance(kwargs["table_format"], str):
        raise TypeError("Keyword argument table_format must be a str.")
    if "return_state" in kwargs and not isinstance(kwargs["return_state"], bool):
        raise TypeError("Keyword argument return_state must be a bool.")
    if "non_blocking" in kwargs:
        if not isinstance(kwargs["non_blocking"], bool):
            raise TypeError("Keyword argument non_blocking must be a bool.")
        debug = True
    if "no_print" in kwargs and not isinstance(kwargs["no_print"], bool):
        raise TypeError("Keyword argument no_print must be a bool.")
    if "bits" in kwargs and not isinstance(kwargs["bits"], int):
        raise TypeError("Keyword argument bits must be an int.")

    path: Path = Path(prog_path)
    if not path.suffix == ".csv":
        raise exceptions.FileNotCSV(path)
    parser.parse_csv(path)
    if "bits" in kwargs:
        assert kwargs["bits"] > 1 and kwargs["bits"] < 8
        global_vars.NUM_BITS_IN_REGISTERS = kwargs["bits"]
        # Don't need to call setup.
        # All it does is change NUM_BITS_IN_REGISTERS and reset globals, which was already done by parse_csv.
    unmapped_addrs_changed: list[int] = []
    if "change" in kwargs:
        for addr in change:
            if addr not in global_vars.RAM:
                unmapped_addrs_changed.append(int(addr))
            if addr < 0:
                raise exceptions.ChangeAddressNegative(addr)
            if addr > global_vars.MAX_PC:
                raise exceptions.ChangeAddressGreaterThan15(addr)
            if (
                change[addr] < 0
                or change[addr] > 2**global_vars.NUM_BITS_IN_REGISTERS - 1
            ):
                raise exceptions.ChangeValueInvalid(change[addr])
            global_vars.RAM[addr] = change[addr]
        if unmapped_addrs_changed:
            print(
                f"WARNING: You attempted to change the following address(es) not mapped in the CSV: {', '.join(list(map(str, unmapped_addrs_changed)))}.\nThis is likely unintentional, but they are now mapped, and the program will continue.",
                file=sys.stderr,
            )
    if "table_format" in kwargs:
        global_vars.table_format = kwargs["table_format"]
    if debug:
        if not kwargs.get("no_print"):
            print(f"Initial state of simulation of {prog_path}")
            helpers.print_RAM()
            helpers.print_info()
            print("Debug mode: press Enter to execute next instruction ( > ).")
        if not kwargs.get("non_blocking"):
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
            if not kwargs.get("no_print"):
                helpers.print_RAM()
                helpers.print_info()
            if not kwargs.get("non_blocking"):
                input()
        print("Program halted.")
    else:
        execute_full_speed()
        if not kwargs.get("no_print"):
            helpers.print_RAM()
            helpers.print_info()

    if kwargs.get("return_state"):
        return helpers.get_state()


@is_documented_by(
    run,
    2,
    "",
    r"""
    :return: ``dict`` containing program state (see ``helpers.get_state``)
    :rtype: ``dict[str, Any]``
    """,
)
def run_and_return_state(prog_path: str, **kwargs: Any) -> dict[str, Any]:
    if (
        "return_state" in kwargs
        and isinstance(kwargs["return_state"], bool)
        and not kwargs["return_state"]
    ):
        print(
            "You called run_and_return_state but set return_state to False????",
            file=sys.stderr,
        )
        exit(1)
    run(prog_path, **kwargs)
    return helpers.get_state()
