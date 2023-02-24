"""Miscellaneous helper functions."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import src.utils.globs as globs
from tabulate import tabulate


def parse_byte(byte: int):
    """Given a byte (2 hexits), return the opcode (1 hexit) and arg (1 hexit). Return as dict for readability."""
    opcode: int = (byte & 0xF0) >> 4
    arg: int = byte & 0xF
    return {"opcode": opcode, "arg": arg}


def parse_opcode(byte: int) -> int:
    """Given a byte, return the 4-bit opcode, just the top 4 bits."""
    return (byte & 0xF0) >> 4


def parse_arg(byte: int) -> int:
    """Given a byte, return the 4-bit arg, just the bottom 4 bits."""
    return byte & 0xF


def print_RAM(**kwargs):
    """Pretty print the contents of RAM, sorted by address. | <PC (optional)> | Addr | Instruction | Dec | Hex | (since we can't distinguish instructions from data). Display arrow on current PC value if `dispPC=True` in kwargs. Set `format=` to set tabulate pretty-print format."""
    table = []
    for addr in sorted(globs.RAM.keys()):
        byte = globs.RAM[addr]
        opcode = parse_opcode(byte)
        arg = parse_arg(byte)
        table_row = []
        if "dispPC" in kwargs and kwargs["dispPC"]:
            table_row.append(">" if globs.PC == addr else "")
        if opcode in globs.OPCODE_TO_MNEMONIC:
            table_row.extend([addr, globs.OPCODE_TO_MNEMONIC[opcode] + " " + str(arg), byte, pad_hex(hex(byte), 2)])
        else:
            table_row.extend([addr, "Invalid Opcode", byte, pad_hex(hex(byte), 2)])
        table.append(table_row)
    headers = []
    if "dispPC" in kwargs and kwargs["dispPC"]:
        headers.append("")
    headers.extend(["Addr", "Instruction", "Dec", "Hex"])
    print(tabulate(table, headers=headers, tablefmt=globs.table_fmt))


def print_info(**kwargs):
    """Print the values of everything in global_vars.py except RAM. Set optional parameter `bool=True` to print flags as `bool` instead of `int`. Set `format=` for tabulate pretty-print format."""
    table = [
        [
            "PC", globs.PC], [
            "Reg A", globs.A], [
                "Reg B", globs.B], [
                    "FlagC", globs.FLAG_C if (
                        "bool" in kwargs and kwargs["bool"]) else int(
                            globs.FLAG_C)], [
                                "FlagZ", globs.FLAG_Z if (
                                    "bool" in kwargs and kwargs["bool"]) else int(
                                        globs.FLAG_Z)]]
    print(tabulate(table, tablefmt=globs.table_fmt))


def pad_hex(hex: str, width: int):
    """Pad given hex str with 0x prefix to width hexits. That is, 0x prefix not included in the width."""
    return '0x' + hex[2:].zfill(width)


def clone_dict(dict):
    """Returns a deep clone of `dict`. Used to clone `RAM`."""
    rv = {}
    for key in dict:
        rv[key] = dict[key]
    return rv


def setup_4bit():
    """Sets up the 4-bit environment and resets global variables to default values."""
    globs.NUM_BITS_IN_REGISTERS = 4
    globs.MAX_UNSIGNED_VAL_IN_REGISTERS = 2 ** 4 - 1
    reset_globals()


def setup_8bit():
    """Sets up the 8-bit environment and resets global variables to default values."""
    globs.NUM_BITS_IN_REGISTERS = 8
    globs.MAX_UNSIGNED_VAL_IN_REGISTERS = 2 ** 8 - 1
    reset_globals()


def setup_n_bit(n: int):
    """Sets up the n-bit environment and resets global variables to default values."""
    assert n > 1
    globs.NUM_BITS_IN_REGISTERS = n
    globs.MAX_UNSIGNED_VAL_IN_REGISTERS = 2 ** n - 1
    reset_globals()


def reset_globals():
    """Reset global variables (not `NUM_BITS_IN_REGISTERS` and `MAX_UNSIGNED_VAL_IN_REGISTERS` to default values."""
    globs.RAM = {}
    globs.PC = 0
    globs.A = 0
    globs.B = 0
    globs.FLAG_C = False
    globs.FLAG_Z = False
    globs.EXECUTING = True


def check_state_all(RAM, PC: int, A: int, B: int, FLAG_C: bool, FLAG_Z: bool, EXECUTING: bool):
    """Compare all current state variables to expected values. Mostly used in testing functions."""
    assert RAM == globs.RAM
    assert PC == globs.PC
    assert A == globs.A
    assert B == globs.B
    assert FLAG_C == globs.FLAG_C
    assert FLAG_Z == globs.FLAG_Z
    assert EXECUTING == globs.EXECUTING


def check_state(**kwargs):
    """Compare the current state to expected values. Mostly used in testing functions.
    Optional parameters RAM=, PC=, A=, B=, FLAG_C=, FLAG_Z=, EXECUTING="""
    if 'RAM' in kwargs:
        assert kwargs['RAM'] == globs.RAM
    if 'PC' in kwargs:
        assert kwargs['PC'] == globs.PC
    if 'A' in kwargs:
        assert kwargs['A'] == globs.A
    if 'B' in kwargs:
        assert kwargs['B'] == globs.B
    if 'FLAG_C' in kwargs:
        assert kwargs['FLAG_C'] == globs.FLAG_C
    if 'FLAG_Z' in kwargs:
        assert kwargs['FLAG_Z'] == globs.FLAG_Z
    if 'EXECUTING' in kwargs:
        assert kwargs['EXECUTING'] == globs.EXECUTING
