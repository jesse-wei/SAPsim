"""Global variables.

If changing anything in this file, also modify ``SAPsim/__init__.py`` and ``helpers.print_info``."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from bidict import bidict

RAM = {}
"""``dict[int, int]`` mapping ``PC``:``byte``, where ``byte`` can be instruction or data (indistinguishable, mostly)"""
PC: int = 0
"""Program counter that indexes into ``RAM``, default value 0"""
A: int = 0
"""Register A, default value 0"""
B: int = 0
"""Register B, default value 0"""
FLAG_C: bool = False
"""Carry-out bit, modified by ``add()`` and ``sub()``. Default value False (0)."""
FLAG_Z: bool = False
"""Zero flag = NOR(Sum bits), modified by ``add()`` and ``sub()``. Default value False (0).

Lab 3's ALU has default value True (1) for FlagZ because the results register is initially 0.

However, it makes more sense in the simulation to set it to False by default."""

# Number of bits in registers
# Same as number of full adders
# This affects how FLAG_C, FLAG_Z, and result register work
NUM_BITS_IN_REGISTERS: int = 8
"""This variable is the #bits in registers and affects how ``add``, ``sub``, ``ldi``, and ``lda`` work.
Default value is 8."""
EXECUTING: bool = True
"""Is the program executing? Set to ``False`` by ``hlt()``"""

MNEMONIC_TO_OPCODE: bidict = bidict(
    {
        "NOP": 0,
        "LDA": 1,
        "ADD": 2,
        "SUB": 3,
        "STA": 4,
        "LDI": 5,
        "JMP": 6,
        "JC": 7,
        "JZ": 8,
        "OUT": 14,
        "HLT": 15,
    }
)

"""Bidirectional dictionary mapping ``str mnemonic : int opcode``.

Use ``MNEMONIC_TO_OPCODE.inverse[opcode]`` to get mnemonic from opcode.

All mnemonics in this dict are in all caps."""

table_format: str = "simple_outline"
"""Tabulate ``table_fmt`` arg to customize pretty-printing. Defaults to ``simple_outline``, see all options: https://github.com/astanin/python-tabulate#table-
                        format"""
