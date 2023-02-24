# SAPsim

> Simulation of [SAP (Simple As Possible) computer](img/SAP.png) programs from COMP311 @ [UNC](https://unc.edu)

![Tests](https://github.com/jesse-wei/SAPsim/actions/workflows/tests.yml/badge.svg)

Write a SAP program in the format given in [`template.csv`](template.csv). Also see [`example.csv`](tests/public_prog/example.csv) ([output](tests/data/public_prog/example_expected.txt)).

You may edit the `.csv` files in Microsoft Excel. Pass the path to your program as a CLI arg. It'll then be [parsed](#parsing-rules) and run at full speed (default), with only final program state displayed, or in debug mode, where program state will be shown after each instruction.

First, make sure you're running Python 3.7+ with `python --version`. If not, try `python3 --version` and replace every `python` with `python3` from now on.

Then, run `python -m pip install -r requirements.txt`.

```
usage: python -m main [-h] [-d] [-b BITS] [-f FORMAT] prog

positional arguments:
  prog                  path to SAP program in the format given in template files

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
  - The parser allows you to map addresses greater than 15, but if something breaks, it's probably due to this limitation.
    - For example, if you have data at `Address` 30 and attempt to run `LDA 30`, the `Arg` does not fit in a hexit, so the instruction no longer fits in a byte. As in SAP, this program assumes everything in RAM is a byte.
    - You could probably have a working program that's longer than 16 addresses as long as you avoid the above issue, though I haven't tested this.
- Initial values are `{PC: 0, Register A: 0, Register B: 0, FlagC: 0, FlagZ: 0, num_bits_in_registers: 8, Executing: 1}`.
- `A` and `B` registers are unsigned. They're 8-bit by default, and this is configurable via the `-b BITS` CLI option.
  - This means, for an 8-bit example, $0-1=255$, and $255+2=1$.
  - If this doesn't make sense, play around with the ALU you made in Lab 3! That's the best way to learn these concepts.
  - Also see the [unsigned comparison table for ALU subtraction](/img/unsigned_comparison_table_ALU_subtraction.png).
- Programs run until they `HLT` or until an [Exception](src/utils/exceptions.py) is raised. Infinite loops are possible, of course.
- Real SAP programs don't have comments, but comments are allowed and encouraged in the `Comments` column of the `.csv` programs!
- These are the same rules a SAP computer implemented by hardware has to follow.
  - > "This is a feature, not a bug"

## Parsing rules

### How to avoid parsing issues

- See [`example.csv`](tests/public_prog/example.csv) ([output](tests/data/public_prog/example_expected.txt)).
  - **No blank rows**
  - But it's fine to have an `Address` with no `Mnemonic` **and** no `Arg`, which is pretty much a blank row
    - For example, note that `Address`es 10 and 11 are mapped but otherwise blank. So `NOP 0` is automatically inserted into RAM at `Address`es 10 and 11.
    - If that's annoying, then skip the `Address`.
  - It's mostly fine to skip `Address`es
    - For example, note that `Address`es 7 and 10 are mapped but not 8 and 9.
    - The skipped `Address`es 8 and 9 are not mapped and appear blank in RAM.
    - If a skipped `Address` is executed (i.e. `PC` == `unmapped Address`), then the program will act as if there's a `NOP` there and just do `PC += 1`.
      - For example, note the `OUT` at `Address` 7 is executed, and execution continues until the `HLT` at `Address` 12.

### How to get a parsing `Exception`

- No `Address` in a row
- Completely blank row
- An `Address` in a row with a `Mnemonic` XOR `Arg`
  - 4-bit data could be represented as an `Arg` with no `Mnemonic`. Similarly, the `Arg` field for `NOP`, `OUT`, and `HLT` don't matter, so these three instructions don't necessarily need an `Arg`.
  - However, in SAP, all instructions/data are represented as a byte, so the parser does not allow just one or the other.
    - This is why each byte in RAM is displayed as both an instruction and data (dec and hex). The program can't tell which one it is.
- Duplicate `Address`es
- 4-bit opcode in a `Mnemonic` field

## [Exceptions](src/utils/exceptions.py)

- See the link in this heading for a list of custom Exceptions. The names are self-explanatory, and there are also error messages.
