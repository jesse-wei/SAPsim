"""Entrypoint of program. Usage: `python -m src.main [-h] [-d] [-b BITS] [-f FORMAT] prog.csv`"""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from src.utils.parser import parse_csv, parse_cli
import src.utils.helpers as helpers
import src.utils.globs as globs
import src.utils.execute as execute


def main():
    args = parse_cli()
    parse_csv(args.prog)

    if args.bits:
        if int(args.bits) <= 1:
            print(f"-b, --bits argument must be greater than 1!\nExiting.")
            exit(1)
        globs.NUM_BITS_IN_REGISTERS = int(args.bits)
        globs.MAX_UNSIGNED_VAL_IN_REGISTERS = 2 ** int(args.bits) - 1

    if args.format:
        globs.table_fmt = args.format

    # Run program
    globs.PC = 0
    globs.EXECUTING = True
    # Debug mode
    if args.debug:
        print("Initial state of simulation.")
        helpers.print_RAM(dispPC=True)
        helpers.print_info()
        print("Debug mode: press Enter to execute next instruction ( > ) and display info.")
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
    # Run to completion or to Exception
    else:
        execute.execute_full_speed()
        helpers.print_RAM()
        helpers.print_info()
        print("Program halted.")


if __name__ == "__main__":
    main()
