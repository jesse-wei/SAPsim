"""Miscellaneous helper functions."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"


from tabulate import tabulate
from typing import Any
import SAPsim.utils.global_vars as global_vars
import SAPsim.utils.exceptions as exceptions


def is_documented_by(
    original, lines_to_remove: int = 0, prepend: str = "", append: str = ""
):
    r"""Use for wrapper functions that should have the original function's docstring.

    :param original: The original function
    :param lines_to_remove: How many lines to remove from the end of the docstring (i.e., to remove old return)
    :type lines_to_remove: ``int``
    :param preprend: What to prepend to docstring. Pass in a docstring (i.e., triple quotation marks), and there should be a trailing newline
    :type prepend: ``str``
    :param append: What to append to docstring. Pass in a docstring (i.e., triple quotation marks), and there should be a leading newline
    :type append: ``str``"""

    def wrapper(target):
        original_doc = original.__doc__.rstrip("\n")
        target.__doc__ = "\n".join(original_doc.split("\n")[:-lines_to_remove])
        # append_with_newline = append
        # if append_with_newline and append_with_newline[0] != "\n":
        #     append_with_newline = "\n" + append_with_newline
        target.__doc__ = f"{prepend}{target.__doc__}"
        target.__doc__ += f"{append}"
        return target

    return wrapper


def parse_byte(byte: int):
    """Given a byte (2 hexits), return the opcode (1 hexit) and arg (1 hexit). Return as dict for readability.

    :param byte:
    :type byte: int
    :return: {'opcode': opcode, 'arg': arg}
    :rtype: dict[str, int]"""
    opcode: int = (byte & 0xF0) >> 4
    arg: int = byte & 0xF
    return {"opcode": opcode, "arg": arg}


def parse_opcode(byte: int):
    """Given a byte, return the 4-bit opcode, just the top 4 bits.

    :param byte:
    :type byte: int
    :return: 4-bit opcode
    :rtype: int"""
    return (byte & 0xF0) >> 4


def parse_arg(byte: int) -> int:
    """Given a byte, return the 4-bit arg, just the bottom 4 bits.

    :param byte:
    :type byte: int
    :return: 4-bit arg
    :rtype: int"""
    return byte & 0xF


def instruction_to_byte(instruction: str) -> int:
    """Given an instruction in the form <Mnemonic> <Arg>, with a space, return the byte representation.

    For NOP, OUT, and HLT, if an Arg is not given, then the right hexit will just be 0.

    Haven't yet tested exception handling."""
    if " " not in instruction:
        if len(instruction) != 3 or instruction.upper() not in {"NOP", "OUT", "HLT"}:
            raise exceptions.InstructionRequiresArg(instruction)
        return global_vars.MNEMONIC_TO_OPCODE[instruction.upper()] << 4
    space_position = instruction.find(" ")
    if len(instruction) != (space_position + 2) and len(instruction) != (
        space_position + 3
    ):
        raise exceptions.InvalidInstructionString(instruction)
    if (
        int(instruction[space_position + 1 :]) < 0
        or int(instruction[space_position + 1 :]) >= 16
    ):
        raise exceptions.InvalidInstructionString(instruction)
    return (
        global_vars.MNEMONIC_TO_OPCODE[instruction[:space_position].upper()] << 4
    ) | int(instruction[space_position + 1 :])


@is_documented_by(
    instruction_to_byte,
    0,
    ""
    r"""
                  Alias for ``instruction_to_byte()``.
                  """,
)
def i2b(instruction: str) -> int:
    return instruction_to_byte(instruction)


def print_RAM():
    """Pretty print the contents of RAM, sorted by address.

    | PC | Addr | Instruction | Dec | Hex |
    Display byte in dec and hex format and attempt to display as instruction (except when opcode invalid)
    for all bytes since we can't distinguish instructions from data.

    Display arrow on current PC value.

    Uses ``global_vars.table_format`` for table format passed to ``tabulate()``."""
    table = []
    for addr in sorted(global_vars.RAM.keys()):
        byte = global_vars.RAM[addr]
        opcode = parse_opcode(byte)
        arg = parse_arg(byte)
        instruction_str = (
            (global_vars.MNEMONIC_TO_OPCODE.inverse[opcode] + " " + str(arg))
            if opcode in global_vars.MNEMONIC_TO_OPCODE.inverse
            else "Invalid Opcode"
        )
        table_row = [
            ">" if global_vars.PC == addr else "",
            addr,
            instruction_str,
            byte,
            pad_hex(hex(byte), 2),
        ]
        table.append(table_row)
    headers = ["PC", "Addr", "Instruction", "Dec", "Hex"]
    print(tabulate(table, headers=headers, tablefmt=global_vars.table_format))


def print_info():
    """Print the values of everything in ``global_vars.py`` except RAM."""
    table = [
        ["PC", global_vars.PC],
        ["Reg A", global_vars.A],
        ["Reg B", global_vars.B],
        ["FlagC", int(global_vars.FLAG_C)],
        ["FlagZ", int(global_vars.FLAG_Z)],
    ]
    print(tabulate(table, tablefmt=global_vars.table_format))


def pad_hex(hex: str, width: int):
    """Pad given hex str with 0x prefix to width hexits. That is, 0x prefix not included in the width."""
    return "0x" + hex[2:].zfill(width)


def clone_dict(dict):
    """Returns a deep clone of ``dict``. Used to clone ``RAM``."""
    rv = {}
    for key in dict:
        rv[key] = dict[key]
    return rv


def setup_4bit():
    """Sets up the 4-bit environment and resets global variables to default values."""
    global_vars.NUM_BITS_IN_REGISTERS = 4
    reset_globals()


def setup_8bit():
    """Sets up the 8-bit environment and resets global variables to default values."""
    global_vars.NUM_BITS_IN_REGISTERS = 8
    reset_globals()


def setup_n_bit(n: int):
    """Sets up the n-bit environment and resets global variables to default values."""
    assert n > 1
    global_vars.NUM_BITS_IN_REGISTERS = n
    reset_globals()


def reset_globals():
    """Reset global variables (not ``NUM_BITS_IN_REGISTERS``) to default values."""
    global_vars.RAM = {}
    global_vars.PC = 0
    global_vars.A = 0
    global_vars.B = 0
    global_vars.FLAG_C = False
    global_vars.FLAG_Z = False
    global_vars.EXECUTING = True


def get_state() -> dict[str, Any]:
    """Return a dict of global variables and their values.
    Mostly used in testing functions."""
    return {
        "RAM": global_vars.RAM,
        "PC": global_vars.PC,
        "A": global_vars.A,
        "B": global_vars.B,
        "FLAG_C": global_vars.FLAG_C,
        "FLAG_Z": global_vars.FLAG_Z,
        "EXECUTING": global_vars.EXECUTING,
    }


def check_state_all(
    RAM, PC: int, A: int, B: int, FLAG_C: bool, FLAG_Z: bool, EXECUTING: bool
):
    """Compare all current state variables to expected values. Mostly used in testing functions."""
    assert RAM == global_vars.RAM
    assert PC == global_vars.PC
    assert A == global_vars.A
    assert B == global_vars.B
    assert FLAG_C == global_vars.FLAG_C
    assert FLAG_Z == global_vars.FLAG_Z
    assert EXECUTING == global_vars.EXECUTING


def check_state(**kwargs):
    """Compare the current state to expected values. Mostly used in testing functions.

    Optional parameters RAM=, PC=, A=, B=, FLAG_C=, FLAG_Z=, EXECUTING="""
    if "RAM" in kwargs:
        assert kwargs["RAM"] == global_vars.RAM
    if "PC" in kwargs:
        assert kwargs["PC"] == global_vars.PC
    if "A" in kwargs:
        assert kwargs["A"] == global_vars.A
    if "B" in kwargs:
        assert kwargs["B"] == global_vars.B
    if "FLAG_C" in kwargs:
        assert kwargs["FLAG_C"] == global_vars.FLAG_C
    if "FLAG_Z" in kwargs:
        assert kwargs["FLAG_Z"] == global_vars.FLAG_Z
    if "EXECUTING" in kwargs:
        assert kwargs["EXECUTING"] == global_vars.EXECUTING
