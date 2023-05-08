"""Parses a SAP program in the CSV format given in ``template.csv`` into ``global_vars.RAM``."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from csv import DictReader
from pathlib import Path
import SAPsim.utils.exceptions as exceptions
import SAPsim.utils.global_vars as global_vars


def parse_csv(file_path: Path):
    """Takes a ``.csv`` file path in ``template.csv`` format and parses it into ``RAM``."""
    prog = DictReader(open(file_path))
    num_rows = 1
    addresses = set()

    for row in prog:
        if not row["Address"]:
            raise exceptions.RowWithNoAddress(num_rows)
        address = 0
        try:
            address = int(row["Address"])
        except ValueError:
            # Must be hex string here
            try:
                address = int(row["Address"], 16)
            except ValueError:
                raise exceptions.InvalidAddress(num_rows)
        if address < 0:
            raise exceptions.NegativeAddress(num_rows)
        num_rows += 1

        if address in addresses:
            raise exceptions.DuplicateAddress(address)
        addresses.add(address)

        # If there's an Address and no First Hexit and no Second Hexit in a row, insert a NOP 0 and continue parsing
        if not row["First Hexit"] and not row["Second Hexit"]:
            global_vars.RAM[address] = 0x00
            continue
        # But if there's an Address and either only an First Hexit or only an Second Hexit, exception
        elif row["First Hexit"] and not row["Second Hexit"]:
            raise exceptions.NoSecondHexit(address)
        elif not row["First Hexit"] and row["Second Hexit"]:
            raise exceptions.NoFirstHexit(address)

        first_hexit = 0
        # Need to determine if the field is a base-10 int or one-letter hexit str or First Hexit str.
        # int() will cause a ValueError if it's a one-letter hexit str or First Hexit str.
        try:
            # int() strips the str
            first_hexit = int(row["First Hexit"])
            # Must be a valid base-10 integer here
            if first_hexit < 0:
                raise exceptions.FirstHexitNegative(address)
            elif first_hexit > 0xF:
                raise exceptions.FirstHexitGreaterThan15(address)
        except ValueError:
            # Must be a string, First Hexit or hexit
            # Use strip() and upper() for some safety
            first_hexit = row["First Hexit"].strip().upper()
            # Must be a hex value if length is 1
            if len(first_hexit) == 1:
                try:
                    first_hexit = int(first_hexit, 16)
                except ValueError:
                    raise exceptions.InvalidFirstHexit(address)
            # Otherwise must be First Hexit
            else:
                if first_hexit not in global_vars.MNEMONIC_TO_OPCODE:
                    raise exceptions.InvalidFirstHexit(address)
                first_hexit = global_vars.MNEMONIC_TO_OPCODE[first_hexit]

        second_hexit = 0
        try:
            second_hexit = int(row["Second Hexit"])
            # Must be a base-10 integer here
            if second_hexit < 0:
                raise exceptions.SecondHexitNegative(address)
            elif second_hexit > 0xF:
                raise exceptions.SecondHexitGreaterThan15(address)
        except ValueError:
            # Must be a str here
            # Use strip() and upper() for some safety for a string field
            arg = row["Second Hexit"].strip().upper()
            if len(arg) != 1:
                raise exceptions.InvalidSecondHexit(address)
            try:
                second_hexit = int(arg, 16)
            except ValueError:
                raise exceptions.InvalidSecondHexit(address)

        byte = first_hexit << 4 | second_hexit
        global_vars.RAM[address] = byte

    if len(global_vars.RAM) > 16:
        raise exceptions.MoreThan16MappedAddresses
