# SAPsim

> Simulation of [SAP (Simple As Possible) computer](img/SAP.png) programs from COMP311 @ [UNC](https://unc.edu)

![Tests](https://github.com/jesse-wei/SAPsim/actions/workflows/tests.yml/badge.svg)

Write a SAP program in the format given in [`template.csv`](template.csv). Also see [`example.csv`](tests/public_prog/example.csv) ([output full speed](tests/data/public_prog/example_full_speed.txt)) ([output debug mode](tests/data/public_prog/example_debug.txt)).

You may edit the `.csv` files in Microsoft Excel. Pass the path to your SAP program as a CLI arg. It'll then be parsed and run at full speed (default), and only the final program state will be displayed. Alternatively, apply the `-d` flag to run in debug mode, which displays program state after each instruction.

First, make sure you're running Python 3.7+ with `python3 --version`.

Then, run `python3 -m pip install -r requirements.txt`. Use a [virtual environment](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments) if you're cool.

```
usage: python -m main [-h] [-d] [-b BITS] [-f FORMAT] prog

positional arguments:
  prog                  path to SAP program in the format given in template.csv

options:
  -h, --help            show this help message and exit
  -d, --debug           debug/step mode
  -b BITS, --bits BITS  number of bits in the ***unsigned*** registers (default is 8)
  -f FORMAT, --format FORMAT
                        print format, options: https://github.com/astanin/python-tabulate#table-format, modify default value in
                        src/utils/globs.py
```

This program passes all my unit tests (many omitted here) on `[3.7, 3.8, 3.9, 3.10]` $\times$ `[ubuntu-latest, windows-latest]`.

![SAP instruction set](img/SAP_instruction_set.png)

## General rules for SAP programs

- All SAP programs should fit in 16 addresses (0 to 15) because the program counter (`PC`) is 4-bit.
- Initial values are `{PC: 0, Register A: 0, Register B: 0, FlagC: 0, FlagZ: 0, num_bits_in_registers: 8, Executing: 1}`.
- `A` and `B` registers are unsigned and 8-bit by default. This is configurable via the `-b BITS` CLI option.
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

- See [`example.csv`](tests/public_prog/example.csv) ([output](tests/data/public_prog/example_full_speed.txt)).
  - **No blank rows**
  - But it's fine to have an `Address` with no `Mnemonic` **and** no `Arg`, which is pretty much a blank row
  - It's fine to skip `Address`es

### How to get a parsing `Exception`

- No `Address` in a row
- Completely blank row
- An `Address` in a row with a `Mnemonic` XOR `Arg` (i.e., missing just one)
- Duplicate `Address`es
- 4-bit opcode in a `Mnemonic` field
- Mnemonic (if numerical) or Arg doesn't fit in a hexit

## [Exceptions](src/utils/exceptions.py)

- See the link in the heading for a list of custom Exceptions. The names are self-explanatory.
