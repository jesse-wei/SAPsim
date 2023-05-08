"""SAP instruction implementation.

All function docstrings (and even most implementations) are ripped straight from the SAP Instruction Set,
with only slight modifications.

This DOES NOT exist in actual SAP but for the purposes of simulation and testing,
``add(arg)`` and ``sub(arg)`` have optional kwargs ``direct_add=`` and ``direct_sub=``
that will cause ``A = A + arg``, ``A = A - arg`` instead of ``A = A + Mem(arg)``, ``A = A - Mem(arg)``.

This DOES NOT exist in actual SAP but for implementation purposes, instructions that don't need an
arg (i.e. NOP, OUT, HLT) get a default parameter so that they can still be called with an argument.
In actual SAP, all instructions (byte) have a required Arg, not a default or optional arg.

``OPCODE_TO_INSTR_PROCEDURE`` dict that maps opcodes to procedures is defined at the bottom."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from tabulate import tabulate
import SAPsim.utils.global_vars as global_vars
import SAPsim.utils.exceptions as exceptions
import SAPsim.utils.helpers as helpers


def nop(arg: int = 0) -> None:
    """Nop

    Opcode 0"""
    global_vars.PC += 1


def lda(arg: int) -> None:
    """``A = Mem(arg)``

    Opcode 1"""
    if arg not in global_vars.RAM:
        raise exceptions.LoadFromUnmappedAddress
    global_vars.A = global_vars.RAM[arg]
    if global_vars.A > (2**global_vars.NUM_BITS_IN_REGISTERS - 1):
        raise exceptions.ARegisterNotEnoughBits
    if global_vars.A < 0:
        raise exceptions.ARegisterNegativeInt
    global_vars.PC += 1


def add(arg: int, **kwargs) -> None:
    """``A = A + Mem(arg)``. Accounts for ``NUM_BITS_IN_REGISTERS`` to set ``FLAG_C`` and ``FLAG_Z``. Handles overflow.

    Opcode 2

    Parameters
    ----------
    arg: int
        memory address, usually
    kwarg
        ``direct_add``: bool
            Set to ``True`` to directly add ``arg`` (i.e. ``A = A + arg`` instead of ``A = A + Mem(arg)``), for testing purposes and use in ``sub``.

            This behavior does not exist in actual SAP."""
    if "direct_add" in kwargs and kwargs["direct_add"]:
        global_vars.B = arg
    else:
        if arg not in global_vars.RAM:
            raise exceptions.LoadFromUnmappedAddress
        global_vars.B = global_vars.RAM[arg]

    if global_vars.B > (2**global_vars.NUM_BITS_IN_REGISTERS - 1):
        raise exceptions.BRegisterNotEnoughBits
    if global_vars.B < 0:
        raise exceptions.BRegisterNegativeInt

    global_vars.A += global_vars.B

    if global_vars.A > (2**global_vars.NUM_BITS_IN_REGISTERS - 1):
        global_vars.FLAG_C = 1
        global_vars.A -= 2**global_vars.NUM_BITS_IN_REGISTERS
    else:
        global_vars.FLAG_C = 0
    global_vars.FLAG_Z = global_vars.A == 0

    global_vars.PC += 1


def sub(arg: int, **kwargs) -> None:
    """``A = A - Mem(arg)``. Accounts for ``NUM_BITS_IN_REGISTERS`` to set ``FLAG_C`` and ``FLAG_Z``. Calls ``add()`` twice to perform 2's complement subtraction.

    Opcode 3

    Parameters
    ----------
    arg: int
        memory address, usually
    kwarg
        direct_sub: bool
            set to ``True`` to directly sub ``arg`` (i.e. ``A = A - arg`` instead of ``A = A - Mem(arg)``), for testing purposes.

            This behavior does not exist in actual SAP."""
    if "direct_sub" in kwargs and kwargs["direct_sub"]:
        global_vars.B = arg
    else:
        if arg not in global_vars.RAM:
            raise exceptions.LoadFromUnmappedAddress
        global_vars.B = global_vars.RAM[arg]

    if global_vars.B > (2**global_vars.NUM_BITS_IN_REGISTERS - 1):
        raise exceptions.BRegisterNotEnoughBits
    if global_vars.B < 0:
        raise exceptions.BRegisterNegativeInt

    # Clone A and B for use later in setting FlagC.
    A_clone = global_vars.A
    B_clone = global_vars.B

    inverse_B = B_clone ^ (2**global_vars.NUM_BITS_IN_REGISTERS - 1)

    add(inverse_B, direct_add=True)
    add(1, direct_add=True)

    # add() modified globs.B, reset it
    global_vars.B = B_clone

    # FLAG_Z is correct at this point.
    # FLAG_C is not correct so is explicitly handled.
    # This uses the unsigned comparison table FlagC = A >= B (compare their values before A changed)
    global_vars.FLAG_C = A_clone >= B_clone

    # Subtract 1 from PC since there were 2 adds that each did PC += 1
    # Net effect is globs.PC += 1
    global_vars.PC -= 1


def sta(arg: int) -> None:
    """``Mem(Arg) = A``. CAN store to unmapped addr, which will simply map the addr in RAM.

    Opcode 4"""
    global_vars.RAM[arg] = global_vars.A
    global_vars.PC += 1


def ldi(arg: int) -> None:
    """``A = arg``

    Opcode 5"""
    global_vars.A = arg
    if arg > (2**global_vars.NUM_BITS_IN_REGISTERS - 1):
        raise exceptions.ARegisterNotEnoughBits
    if arg < 0:
        raise exceptions.ARegisterNegativeInt
    global_vars.PC += 1


def jmp(arg: int) -> None:
    """``PC = arg``

    Opcode 6"""
    if arg < 0:
        raise exceptions.JumpToNegativeAddress
    global_vars.PC = arg


def jc(arg: int) -> None:
    """If ``FC=1`` then ``PC=arg``; else go on

    Opcode 7"""
    if global_vars.FLAG_C:
        if arg < 0:
            raise exceptions.JumpToNegativeAddress
        global_vars.PC = arg
    else:
        global_vars.PC += 1


def jz(arg: int) -> None:
    """If ``FZ=1`` then ``PC=arg``; else go on

    Opcode 8"""
    if global_vars.FLAG_Z:
        if arg < 0:
            raise exceptions.JumpToNegativeAddress
        global_vars.PC = arg
    else:
        global_vars.PC += 1


def out(arg: int = 0) -> None:
    """``Display = OUT = A``. Prints | PC | A (dec) | A (hex) |

    Opcode 14"""
    arg = helpers.parse_arg(global_vars.RAM[global_vars.PC])
    table = [[global_vars.PC, global_vars.A, helpers.pad_hex(hex(global_vars.A), 2)]]
    print(
        tabulate(table, headers=["PC", "Dec", "Hex"], tablefmt=global_vars.table_format)
    )
    global_vars.PC += 1


def hlt(arg: int = 0) -> None:
    """Halt

    Opcode 15"""
    global_vars.EXECUTING = False


OPCODE_TO_INSTR_PROCEDURE = {
    0: nop,
    1: lda,
    2: add,
    3: sub,
    4: sta,
    5: ldi,
    6: jmp,
    7: jc,
    8: jz,
    14: out,
    15: hlt,
}
"""This ``dict`` maps opcodes to the procedures defined in this file.

The syntax ``OPCODE_TO_INSTR_PROCEDURE[opcode](arg)`` will execute the correct instruction with ``arg`` passed as argument! Very cool."""
