"""Parses a SAP program in the CSV format given in `template.csv` into `globs.RAM`."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import argparse
from src.utils.helpers import *
from csv import DictReader
import src.utils.exceptions as exceptions


def parse_cli():
    """Parse cli args using argparse, return parser.parse_args() to main()"""
    parser = argparse.ArgumentParser(usage='python -m sim [-h] [-s] [-c CHANGE] [-f FORMAT] [-b BITS] prog')
    parser.add_argument('prog', help='path to SAP program in the format given in template.csv')
    parser.add_argument('-s', '--speed',
                        help='run at full speed',
                        action="store_true")
    parser.add_argument('-c', '--change',
                        help='before execution, overwrite data at mapped address(es) to base-10 value(s), format is <addr>:<base-10 value>,<addr>:<base-10 value>,...')
    parser.add_argument('-f', '--format',
                        help="print format, options: https://github.com/astanin/python-tabulate#table-format, modify default value in src/utils/globs.py")
    parser.add_argument('-b', '--bits',
                        help='number of bits in the unsigned registers (default is 8)')
    args = parser.parse_args()

    final_dot_position = args.prog.rfind('.')
    if final_dot_position == -1 or args.prog[final_dot_position+1:] != 'csv':
        raise exceptions.InvalidFileExtension(args.prog)

    if args.bits and int(args.bits) <= 1:
        print(f"-b, --bits argument must be greater than 1!\nExiting.")
        exit(1)

    return args


def parse_csv(file_path):
    """Takes a `.csv` file path in `template.csv` format and parses it into `RAM`."""
    prog = DictReader(open(file_path))
    num_rows = 1
    addresses = set()

    for row in prog:
        if not row["Address"]:
            raise exceptions.RowWithNoAddress(num_rows)
        address = 0
        try:
            address = int(row['Address'])
        except ValueError:
            # Must be hex string here
            try:
                address = int(row['Address'], 16)
            except ValueError:
                raise exceptions.InvalidAddress(num_rows)
        if address < 0:
            raise exceptions.NegativeAddress(num_rows)
        num_rows += 1

        if address in addresses:
            raise exceptions.DuplicateAddress(address)
        addresses.add(address)

        # If there's an Address and no Mnemonic and no Arg in a row, insert a NOP 0 and continue parsing
        if not row['Mnemonic'] and not row['Arg']:
            globs.RAM[address] = 0x00
            continue
        # But if there's an Address and either only an Mnemonic or only an Arg, exception
        elif row['Mnemonic'] and not row['Arg']:
            raise exceptions.MnemonicButNoArg(address)
        elif not row['Mnemonic'] and row['Arg']:
            raise exceptions.ArgButNoMnemonic(address)

        first_hexit = 0
        # Need to determine if the field is a base-10 int or one-letter hexit str or Mnemonic str.
        # int() will cause a ValueError if it's a one-letter hexit str or Mnemonic str.
        try:
            # int() strips the str
            first_hexit = int(row['Mnemonic'])
            # Must be a valid base-10 integer here
            if first_hexit < 0:
                raise exceptions.FirstHexitNegative(address)
            elif first_hexit > 0xf:
                raise exceptions.FirstHexitGreaterThan15(address)
        except ValueError:
            # Must be a string, mnemonic or hexit
            # Use strip() and upper() for some safety
            mnemonic = row['Mnemonic'].strip().upper()
            # Must be a hex value if length is 1
            if len(mnemonic) == 1:
                try:
                    first_hexit = int(mnemonic, 16)
                except ValueError:
                    raise exceptions.InvalidFirstHexit(address)
            # Otherwise must be Mnemonic
            else:
                if mnemonic not in globs.MNEMONIC_TO_OPCODE:
                    raise exceptions.InvalidMnemonic(address)
                first_hexit = globs.MNEMONIC_TO_OPCODE[mnemonic]

        second_hexit = 0
        try:
            second_hexit = int(row['Arg'])
            # Must be a base-10 integer here
            if second_hexit < 0:
                raise exceptions.SecondHexitNegative(address)
            elif second_hexit > 0xf:
                raise exceptions.SecondHexitGreaterThan15(address)
        except ValueError:
            # Must be a str here
            # Use strip() and upper() for some safety for a string field
            arg = row['Arg'].strip().upper()
            if len(arg) != 1:
                raise exceptions.InvalidArg(address)
            try:
                second_hexit = int(arg, 16)
            except ValueError:
                raise exceptions.InvalidArg(address)

        byte = first_hexit << 4 | second_hexit
        globs.RAM[address] = byte

    if len(globs.RAM) > 16:
        raise exceptions.MoreThan16MappedAddresses
