"""Test helpers.py."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import pytest
from SAPsim.utils.helpers import *
from SAPsim.utils.globs import *
import SAPsim.utils.exceptions as exceptions


def test_instruction_to_byte_returns_correct_byte():
    """Generate all possible instructions in byte form. Test that `instruction_to_byte` returns the correct byte given the string representation <Mnemonic> <Arg>."""
    # Instructions 0x00 to 0x8f (inclusive)
    for i in range(0x90):
        assert i == instruction_to_byte(
            f"{OPCODE_TO_MNEMONIC[(i & 0xF0) >> 4]} {i & 0xF}"
        )
    # Instructions 0xe0 to 0xff (inclusive)
    for i in range(0xE0, 0xFF):
        assert i == instruction_to_byte(
            f"{OPCODE_TO_MNEMONIC[(i & 0xF0) >> 4]} {i & 0xF}"
        )


def test_instruction_to_byte_NOP_OUT_HLT():
    """Test that instruction to byte returns correct opcode and Arg 0 for NOP, OUT, HLT without an arg."""
    assert 0 == instruction_to_byte("NOP")
    assert 0xE << 4 == instruction_to_byte("OUT")
    assert 0xF << 4 == instruction_to_byte("HLT")


def test_instruction_to_byte_instructions_require_arg():
    instructions_require_arg = ["LDA", "ADD", "SUB", "STA", "LDI", "JMP", "JC", "JZ"]
    for instruction in instructions_require_arg:
        with pytest.raises(exceptions.InstructionRequiresArg):
            instruction_to_byte(instruction)
