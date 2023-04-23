"""Execute instructions in RAM."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import SAPsim.utils.globs as globs
import SAPsim.utils.instructions as instructions
import SAPsim.utils.helpers as helpers
import SAPsim.utils.exceptions as exceptions


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
