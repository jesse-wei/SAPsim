# SAPsim

> Simulation of [SAP (Simple As Possible) computer](img/SAP.png) programs from COMP311 (Computer Organization) @ [UNC](https://unc.edu)

![Tests](https://github.com/jesse-wei/SAPsim/actions/workflows/tests.yml/badge.svg)

Write a SAP program in the format given in [`template.csv`](template.csv). Also see [`example.csv`](tests/public_prog/example.csv) ([output full speed](tests/data/public_prog/example_full_speed.txt)) ([output debug mode](tests/data/public_prog/example_debug.txt)).

You may edit the `.csv` files in Microsoft Excel. Pass the path to your SAP program as a CLI argument. It'll then be run in debug mode (default). Alternatively, apply the `-s` option to run at full <ins>s</ins>peed.

First, make sure your terminal says you're in the `SAPsim/` directory. The current working directory needs to be `.../SAPsim`.

Make sure you're running Python 3.7+ with `python3 --version`.

Then, type `python3 -m pip install -r requirements.txt`.

```
usage: python3 -m sim [-h] [-s] [-c CHANGE] [-f FORMAT] [-b BITS] prog

positional arguments:
  prog                  path to SAP program in the format given in template.csv

options:
  -h, --help            show this help message and exit
  -s, --speed           run at full speed
  -c CHANGE, --change CHANGE
                        before execution, overwrite data at mapped address(es) to base-10 value(s)
                        format is <addr>:<base-10 value>,<addr>:<base-10 value>,...
  -f FORMAT, --format FORMAT
                        print format, options: https://github.com/astanin/python-tabulate#table-format
                        modify default value in src/utils/globs.py
  -b BITS, --bits BITS  number of bits in the unsigned registers (default is 8)
```

This program passes all my unit tests (many omitted here) on `[3.7, 3.8, 3.9, 3.10]` X `[ubuntu-latest, windows-latest]`. I test locally on macOS (M1) with Python 3.10, so that works too.

If you run into `ModuleNotFoundError: No module named 'src'`, make sure your current working directory is `.../SAPsim`!

![SAP instruction set](img/SAP_instruction_set.png)

## General rules for SAP programs

- All SAP programs should fit in 16 addresses (0 to 15) because the program counter (`PC`) is 4-bit.
- Initial values are `{PC: 0, Register A: 0, Register B: 0, FlagC: 0, FlagZ: 0, num_bits_in_registers: 8, Executing: 1}`.
- `A` and `B` registers are unsigned and 8-bit by default. Number of bits is configurable via the `-b BITS` CLI option.
- Any value at a memory address is a byte.
  - An instruction is a Mnemonic representing an Opcode (4-bit) and an Arg (4-bit).
  - All data must fit in a byte. Specifically, the Mnemonic is a base-10 integer representing the first hexit, and the Arg is a base-10 integer representing the second hexit.
    - For example, 255 = `0xFF` is Mnemonic 15, Arg 15.
- Programs run until they `HLT` or until an [Exception](src/utils/exceptions.py) is raised. Infinite loops are possible, of course.
- Real SAP programs don't have comments, but comments are allowed and encouraged in the `Comments` column of the `.csv` programs!
- These are the same rules a SAP computer implemented by hardware has to follow.
  - > "This is a feature, not a bug"

## Parsing rules

### How to avoid parsing issues

- See [`example.csv`](tests/public_prog/example.csv) ([output full speed](tests/data/public_prog/example_full_speed.txt)).
  - It's fine to have an `Address` with no `Mnemonic` **and** no `Arg`, which is pretty much a blank row
  - It's fine to skip `Address`es

### How to get a parsing `Exception`

- No `Address` in a row
- Completely blank row
- An `Address` in a row with a `Mnemonic` XOR `Arg` (i.e., missing just one)
- Duplicate `Address`es
- 4-bit Opcode in a `Mnemonic` field
- Mnemonic (if numerical) or Arg doesn't fit in a hexit

## [Exceptions](src/utils/exceptions.py)

- See the link in the heading for a list of custom Exceptions. The names and messages are self-explanatory.
