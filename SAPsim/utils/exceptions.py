"""Custom exceptions."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import SAPsim.utils.helpers as helpers
import SAPsim.utils.globs as globs


def print_debug_info() -> None:
    """When most Exceptions (not DroppedOffBottom) occur, this function is called to print the instruction that caused the Exception and program state (RAM and registers and flags)"""
    curr_instruction = globs.RAM[globs.PC]
    print(
        f"Exception raised during execution of {globs.OPCODE_TO_MNEMONIC[helpers.parse_opcode(curr_instruction)]} {helpers.parse_arg(curr_instruction)} at address {globs.PC}"
    )
    helpers.print_RAM(dispPC=True)
    helpers.print_info()


class ARegisterNotEnoughBits(Exception):
    """The unsigned value in register A can't be stored in NUM_BITS_IN_REGISTERS bits."""

    def __init__(self):
        self.message = f"The unsigned value in register A can't be stored in {globs.NUM_BITS_IN_REGISTERS} bits."
        print_debug_info()
        super().__init__(self.message)


class BRegisterNotEnoughBits(Exception):
    """The unsigned value in register B can't be stored in NUM_BITS_IN_REGISTERS bits."""

    def __init__(self):
        self.message = f"The unsigned value in register B can't be stored in {globs.NUM_BITS_IN_REGISTERS} bits."
        print_debug_info()
        super().__init__(self.message)


class ARegisterNegativeInt(Exception):
    """There's somehow a negative number in unsigned register A."""

    def __init__(self):
        self.message = (
            f"There's somehow a negative number {globs.A} in unsigned register A."
        )
        print_debug_info()
        super().__init__(self.message)


class BRegisterNegativeInt(Exception):
    """There's somehow a negative number in unsigned register B."""

    def __init__(self):
        self.message = (
            f"There's somehow a negative number {globs.B} in unsigned register B."
        )
        print_debug_info()
        super().__init__(self.message)


class DroppedOffBottom(Exception):
    """Raised if ``PC`` > max address in ``RAM``."""

    def __init__(
        self,
        message=f"PC is greater than max address in RAM. Your program does not always HLT.",
    ):
        self.message = message
        helpers.print_RAM(dispPC=True)
        helpers.print_info()
        super().__init__(self.message)


class LoadFromUnmappedAddress(Exception):
    """Raised if attempting to Mem(addr), but Addr is not mapped."""

    def __init__(self):
        self.message = f"Attempted to load from unmapped address {globs.PC}."
        print_debug_info()
        super().__init__(self.message)


class JumpToNegativeAddress(Exception):
    def __init__(self, message=f"Attempted to jump to a negative address."):
        self.message = message
        print_debug_info()
        super().__init__(self.message)


class InvalidFileExtension(Exception):
    def __init__(
        self,
        path,
        message=f"Invalid file extension for prog positional argument. Must be .csv",
    ):
        self.message = message
        super().__init__(self.message)


class RowWithNoAddress(Exception):
    def __init__(self, row):
        self.message = f"There's a row with no address value in row {row} of your program!\nNote: In Excel, this row might just appear empty, which is normally fine. But open up the .csv in a text editor and you'll see that there is a row with 2 commas but no address value."
        super().__init__(self.message)


class NegativeAddress(Exception):
    def __init__(self, row):
        self.message = f"There's a negative address in row {row} of your program!"
        super().__init__(self.message)


class NonNumericalAddress(Exception):
    def __init__(self, row):
        self.message = f"There's an invalid address (int(address) causes ValueError) in row {row} of your program!"
        super().__init__(self.message)


class InvalidAddress(Exception):
    def __init__(self, row):
        self.message = f"There's an invalid address in row {row} of your program. Address must be a base-10 integer or base-16 hex string."
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
        self.message = (
            f"The first hexit at address {address} of your program must be positive!"
        )
        super().__init__(self.message)


class FirstHexitGreaterThan15(Exception):
    def __init__(self, address):
        self.message = f"The first hexit at address {address} of your program must be less than 16!"
        super().__init__(self.message)


class SecondHexitNegative(Exception):
    def __init__(self, address):
        self.message = (
            f"The second hexit at address {address} of your program must be positive!"
        )
        super().__init__(self.message)


class SecondHexitGreaterThan15(Exception):
    def __init__(self, address):
        self.message = f"The second hexit at address {address} of your program must be less than 16!"
        super().__init__(self.message)


class InvalidFirstHexit(Exception):
    def __init__(self, address):
        self.message = f"The first hexit at address {address} is not valid! Must be a hexit 0 to f or a base-10 integer 0 to 15 representing a hexit. You typed one letter in this field, so I assume you meant to put a hexit here, not a Mnemonic."
        super().__init__(self.message)


class InvalidMnemonic(Exception):
    def __init__(self, address):
        self.message = f"The mnemonic given at address {address} is invalid. See SAP instruction set for list of supported mnemonics. The mnemonic field can also be a hexit 0 to f if representing data."
        super().__init__(self.message)


class InvalidArg(Exception):
    def __init__(self, address):
        self.message = f"The arg at address {address} is invalid. It must be a hexit 0 to f or a base-10 integer 0 to 15 representing a hexit."
        super().__init__(self.message)


class MoreThan16MappedAddresses(Exception):
    def __init__(self):
        self.message = f"A SAP program can have at most 16 addresses! In this simulation, a skipped address doesn't count toward that count. Excluding skipped addresses, you have {len(globs.RAM)} mapped addresses."
        super().__init__(self.message)


class InstructionRequiresArg(Exception):
    def __init__(self, instruction: str):
        self.message = f"You typed: {instruction}. Only NOP, OUT, and HLT strings have an unnecessary Arg (but there's still a hexit for the arg)."
        super().__init__(self.message)


class InvalidInstructionString(Exception):
    def __init__(self, instruction: str):
        self.message = f"Invalid instruction string: {instruction}, correct format is <Mnemonic> <Arg>. NOP, OUT, and HLT strings can have no arg (but there's still a hexit for the arg in the byte representation). Arg must be less than 16."
        super().__init__(self.message)
