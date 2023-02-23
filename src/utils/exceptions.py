"""Custom exceptions."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import src.utils.helpers as helpers
import src.utils.globs as globs


def print_debug_info() -> None:
    """When most Exceptions (not DroppedOffBottom) occur, this function is called to print the instruction that caused the Exception and program state (RAM and registers and flags)"""
    curr_instruction = globs.RAM[globs.PC]
    print(
        f"Exception raised during execution of {globs.OPCODE_TO_MNEMONIC[helpers.parse_opcode(curr_instruction)]} {helpers.parse_arg(curr_instruction)} at address {globs.PC}")
    helpers.print_RAM(dispPC=True)
    helpers.print_info()


class ARegisterNotEnoughBits(Exception):
    """The unsigned value in register A can't be stored in NUM_BITS_IN_REGISTERS bits."""

    def __init__(self, message=f"The unsigned value in register A can't be stored in {globs.NUM_BITS_IN_REGISTERS} bits."):
        self.message = message
        print_debug_info()
        super().__init__(self.message)


class BRegisterNotEnoughBits(Exception):
    """"The unsigned value in register B can't be stored in NUM_BITS_IN_REGISTERS bits."""

    def __init__(self, message=f"The unsigned value in register B can't be stored in {globs.NUM_BITS_IN_REGISTERS} bits."):
        self.message = message
        print_debug_info()
        super().__init__(self.message)


class ARegisterNegativeInt(Exception):
    """There's somehow a negative number in unsigned register A."""

    def __init__(self, message=f"There's somehow a negative number {globs.A} in unsigned register A."):
        self.message = message
        print_debug_info()
        super().__init__(self.message)


class BRegisterNegativeInt(Exception):
    """There's somehow a negative number in unsigned register A."""

    def __init__(self, message=f"There's somehow a negative number {globs.B} in unsigned register B."):
        self.message = message
        print_debug_info()
        super().__init__(self.message)


class DroppedOffBottom(Exception):
    """Raised if `PC` > max address in `RAM`."""

    def __init__(self, message=f"PC is greater than max address in RAM. Your program does not always HLT."):
        self.message = message
        helpers.print_RAM(dispPC=True)
        helpers.print_info()
        super().__init__(self.message)


class LoadFromUnmappedAddress(Exception):
    """Raised if attempting to Mem(addr), but Addr is not mapped."""

    def __init__(self, message=f"Attempted to load from unmapped address {globs.PC}."):
        self.message = message
        print_debug_info()
        super().__init__(self.message)


class JumpToNegativeAddress(Exception):
    def __init__(self, message=f"Attempted to jump to a negative address."):
        self.message = message
        print_debug_info()
        super().__init__(self.message)


class RowWithNoAddress(Exception):
    def __init__(self, row):
        self.message = f"There's a row with no address value in row {row} of your program!\nNote: In Excel, this row might just appear empty, which is normally fine. But open up the .csv in a text editor and you'll see that there is a row with 2 commas but no address value."
        super().__init__(self.message)


class NegativeAddress(Exception):
    def __init__(self, row):
        self.message = f"There's a negative address in row {row} of your program!"
        super().__init__(self.message)


class DuplicateAddress(Exception):
    def __init__(self, address):
        self.message = f"Address {address} is duplicated in your program!"
        super().__init__(self.message)


class MnemonicButNoArg(Exception):
    def __init__(self, address):
        self.message = f"Address {address} of your program has a Mnemonic but no Arg!"
        super().__init__(self.message)


class ArgButNoMnemonic(Exception):
    def __init__(self, address):
        self.message = f"Address {address} of your program has an Arg but no Mnemonic!"
        super().__init__(self.message)


class FirstHexitNegative(Exception):
    def __init__(self, address):
        self.message = f"The first hexit at address {address} of your program must be positive!"
        super().__init__(self.message)


class FirstHexitGreaterThan15(Exception):
    def __init__(self, address):
        self.message = f"The first hexit at address {address} of your program must be less than 16!"
        super().__init__(self.message)


class SecondHexitNegative(Exception):
    def __init__(self, address):
        self.message = f"The second hexit at address {address} of your program must be positive!"
        super().__init__(self.message)


class SecondHexitGreaterThan15(Exception):
    def __init__(self, address):
        self.message = f"The second hexit at address {address} of your program must be less than 16!"
        super().__init__(self.message)


class InvalidMnemonic(Exception):
    def __init__(self, address):
        self.message = f"The mnemonic given at address {address} is invalid. See SAP instruction set for list of supported mnemonics."
        super().__init__(self.message)


class InvalidArg(Exception):
    def __init__(self, address):
        self.message = f"The arg at address {address} is invalid. It must be an integer from 0 to 15, not a string or integer with spaces in between."
        super().__init__(self.message)

class MoreThan16MappedAddresses(Exception):
    def __init__(self):
        self.message = f"A SAP program can have at most 16 addresses! In this simulation, a skipped address doesn't count toward that count. Excluding skipped addresses, you have {len(globs.RAM)} mapped addresses."
        super().__init__(self.message)
