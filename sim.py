"""Entrypoint of program. Usage: python3 -m sim [-h] [-s] [-c CHANGE] [-f FORMAT] [-b BITS] prog"""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from src.utils.parser import parse_csv, parse_cli
import src.utils.helpers as helpers
import src.utils.globs as globs
import src.utils.execute as execute


def main():
    args = parse_cli()
    parse_csv(args.prog)

    # Set up global variables based on CLI args
    if args.bits:
        globs.NUM_BITS_IN_REGISTERS = int(args.bits)
        globs.MAX_UNSIGNED_VAL_IN_REGISTERS = 2 ** int(args.bits) - 1
    if args.change:
        changes = args.change.split(',')
        for change in changes:
            if change.count(':') != 1:
                print("Invalid syntax for --c option, correct format is <addr>:<base-10 value>,<addr>:<base-10 value>, ...")
                exit(1)
            colon_position = change.find(':')
            addr = int(change[:colon_position])
            if addr not in globs.RAM:
                print(f"You can apply a change only to an address that's already mapped (not skipped). Address {addr} is not mapped.")
                exit(1)
            value = int(change[colon_position+1:])
            if value < 0 or value > globs.MAX_UNSIGNED_VAL_IN_REGISTERS:
                print(f"Invalid base-10 value for change: {value}. Negative or overflows registers.")
                exit(1)
            globs.RAM[addr] = value
    if args.format:
        globs.table_fmt = args.format

    # Debug mode (default)
    if not args.speed:
        print("Initial state of simulation.")
        helpers.print_RAM(dispPC=True)
        helpers.print_info()
        print("Debug mode (default): press Enter to execute next instruction ( > ).")
        input()
        while globs.EXECUTING:
            # Special case so that you don't have to press Enter twice to halt on a HLT instruction
            if globs.PC in globs.RAM and helpers.parse_opcode(globs.RAM[globs.PC]) == 0xF:
                execute.execute_next()
                break
            execute.execute_next()
            helpers.print_RAM(dispPC=True)
            helpers.print_info()
            input()
        print("Program halted.")
    # Full speed
    else:
        execute.execute_full_speed()
        helpers.print_RAM()
        helpers.print_info()
        print("Program halted.")


if __name__ == "__main__":
    main()
