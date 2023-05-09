"""Parses a SAP program in the CSV format given in ``template.csv`` into ``global_vars.RAM``."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from csv import DictReader
from pathlib import Path
from typing import Union
import SAPsim.utils.exceptions as exceptions
import SAPsim.utils.global_vars as global_vars
from SAPsim.utils.helpers import setup_state


def parse_csv(file_path: Union[Path, str]) -> None:
    """Takes a ``.csv`` file path in SAPsim ``template.csv`` format and parses it into ``RAM``.

    Calls ``setup_state()`` if ``file_path`` is valid.

    If an address is skipped (not in the ``.csv`` file), it is not mapped in ``RAM``.
    If an address is mapped but First Hexit and Second Hexit are blank, a ``NOP 0`` (0x00) is inserted.

    The reasoning here is that if an addr is skipped completely in the CSV, it shouldn't show up in RAM.
    If an addr is mapped but First Hexit and Second Hexit are blank, it should show up in RAM (as ``NOP 0``).

    :param file_path: The path to the ``.csv`` file to parse.
    :type file_path: Union[Path, str]
    :raises RowWithNoAddress: If a row has no address.
    :raises InvalidAddress: If a row has an invalid address.
    :raises NegativeAddress: If a row has a negative address.
    :raises DuplicateAddress: If a row has a duplicate address.
    :raises NoFirstHexit: If a row has no First Hexit.
    :raises NoSecondHexit: If a row has no Second Hexit.
    :raises FirstHexitNegative: If a row has a negative First Hexit.
    :raises FirstHexitGreaterThan15: If a row has a First Hexit greater than 15.
    :raises SecondHexitNegative: If a row has a negative Second Hexit.
    :raises SecondHexitGreaterThan15: If a row has a Second Hexit greater than 15.
    :raises InvalidFirstHexit: If a row has an invalid First Hexit.
    :raises InvalidSecondHexit: If a row has an invalid Second Hexit.
    :raises MoreThan16MappedAddresses: If there are more than 16 mapped addresses.
    :return: None"""
    prog = DictReader(open(file_path, "r"))
    setup_state()
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

        # If there's an Address and no First Hexit and no Second Hexit in a row
        # insert a NOP 0 at that address and continue parsing
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
