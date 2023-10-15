[![Python 3.9+ badge](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/) [![PyPI version badge](https://badge.fury.io/py/SAPsim.svg)](https://pypi.org/project/SAPsim/) [![tests GitHub action badge](https://github.com/jesse-wei/SAPsim/actions/workflows/tests.yml/badge.svg)](https://github.com/jesse-wei/SAPsim/actions/workflows/tests.yml) [![codecov badge](https://codecov.io/github/jesse-wei/SAPsim/branch/main/graph/badge.svg?token=RS7QI9QVKU)](https://codecov.io/github/jesse-wei/SAPsim) [![documentation badge](https://readthedocs.org/projects/sapsim/badge/?version=latest)](https://SAPsim.readthedocs.io/en/latest/)

# SAPsim

Simulation of SAP (Simple-As-Possible computer) programs from COMP 311 (Computer Organization) @ [UNC](https://unc.edu).

<p align="center">
    <img src="https://raw.githubusercontent.com/jesse-wei/SAPsim/main/docs/_static/SAPsim_demo.gif" alt="SAPsim demo">
</p>

## Install

`pip install SAPsim`

Python 3.9+ is required. If your `pip` command doesn't work, use `pip3` (and consider aliasing `pip` to `pip3`).

## Usage

Write a SAP program in a CSV file in the format shown below. Two commented example programs are in [public_prog/](https://github.com/jesse-wei/SAPsim/tree/main/tests/public_prog), and an empty template is in [template.csv](template.csv).

<p align="center">
    <img src="https://raw.githubusercontent.com/jesse-wei/SAPsim/main/docs/_static/ex1.jpg" alt="Screenshot of ex1.csv in Excel">
</p>
<p align="center">
    <a href="https://github.com/jesse-wei/SAPsim/blob/main/tests/public_prog/ex1.csv">ex1.csv</a>
</p>

To run the SAP program, open a Python terminal and use `SAPsim.run()`.

```py
>>> from SAPsim import run
>>> run("ex1.csv")                  # Run ex1.csv at full speed (default)
┌──────┬────────┬───────────────┬───────┬───────┐
│ PC   │   Addr │ Instruction   │   Dec │ Hex   │
├──────┼────────┼───────────────┼───────┼───────┤
│      │      0 │ LDA 14        │    30 │ 0x1e  │
│      │      1 │ SUB 13        │    61 │ 0x3d  │
│      │      2 │ JZ 6          │   134 │ 0x86  │
│      │      3 │ LDI 0         │    80 │ 0x50  │
│      │      4 │ STA 15        │    79 │ 0x4f  │
│      │      5 │ HLT 0         │   240 │ 0xf0  │
│      │      6 │ LDI 1         │    81 │ 0x51  │
│      │      7 │ STA 15        │    79 │ 0x4f  │
│ >    │      8 │ HLT 0         │   240 │ 0xf0  │
│      │     13 │ NOP 3         │     3 │ 0x03  │
│      │     14 │ NOP 3         │     3 │ 0x03  │
│      │     15 │ NOP 1         │     1 │ 0x01  │
└──────┴────────┴───────────────┴───────┴───────┘
┌───────┬───┐
│ PC    │ 8 │
│ Reg A │ 1 │
│ Reg B │ 3 │
│ FlagC │ 1 │
│ FlagZ │ 1 │
└───────┴───┘
>>> run("ex1.csv", debug=True)      # Run ex1.csv in debug (step) mode
Initial state of simulation of tests/public_prog/ex1.csv
...
Debug mode: press Enter to execute next instruction ( > ).
...
```

**Note**: There is a debug (step) mode that runs one instruction at a time, as shown above. The default behavior is to run at full speed.

### SAP instruction set

<p align="center">
    <img src="https://raw.githubusercontent.com/jesse-wei/SAPsim/main/docs/_static/sap_instruction_set.jpg" alt="SAP instruction set">
</p>

## Settings

To customize table appearance, use `table_format`. [Options](https://github.com/astanin/python-tabulate#table-format).

```py
>>> run("ex1.csv", table_format="github")
| PC   |   Addr | Instruction   |   Dec | Hex   |
|------|--------|---------------|-------|-------|
|      |      0 | LDA 14        |    30 | 0x1e  |
|      |      1 | SUB 13        |    61 | 0x3d  |
|      |      2 | JZ 6          |   134 | 0x86  |
|      |      3 | LDI 0         |    80 | 0x50  |
|      |      4 | STA 15        |    79 | 0x4f  |
|      |      5 | HLT 0         |   240 | 0xf0  |
|      |      6 | LDI 1         |    81 | 0x51  |
|      |      7 | STA 15        |    79 | 0x4f  |
| >    |      8 | HLT 0         |   240 | 0xf0  |
|      |     13 | NOP 3         |     3 | 0x03  |
|      |     14 | NOP 3         |     3 | 0x03  |
|      |     15 | NOP 1         |     1 | 0x01  |
|-------|---|
| PC    | 8 |
| Reg A | 1 |
| Reg B | 3 |
| FlagC | 1 |
| FlagZ | 1 |
```

To modify values in the SAP program without editing the CSV, use the `change` keyword argument.

```py
>>> run("ex1.csv", change={14: 4, 13: 2})      # Change initial byte at address 14 to 4 and at 13 to 2
┌──────┬────────┬───────────────┬───────┬───────┐
│ PC   │   Addr │ Instruction   │   Dec │ Hex   │
├──────┼────────┼───────────────┼───────┼───────┤
│      │      0 │ LDA 14        │    30 │ 0x1e  │
│      │      1 │ SUB 13        │    61 │ 0x3d  │
│      │      2 │ JZ 6          │   134 │ 0x86  │
│      │      3 │ LDI 0         │    80 │ 0x50  │
│      │      4 │ STA 15        │    79 │ 0x4f  │
│ >    │      5 │ HLT 0         │   240 │ 0xf0  │
│      │      6 │ LDI 1         │    81 │ 0x51  │
│      │      7 │ STA 15        │    79 │ 0x4f  │
│      │      8 │ HLT 0         │   240 │ 0xf0  │
│      │     13 │ NOP 2         │     2 │ 0x02  │
│      │     14 │ NOP 4         │     4 │ 0x04  │
│      │     15 │ NOP 0         │     0 │ 0x00  │
└──────┴────────┴───────────────┴───────┴───────┘
┌───────┬───┐
│ PC    │ 5 │
│ Reg A │ 0 │
│ Reg B │ 2 │
│ FlagC │ 1 │
│ FlagZ │ 0 │
└───────┴───┘
```

## Rules

It's easy to just mimic the [example programs](https://github.com/jesse-wei/SAPsim/tree/main/tests/public_prog), but if you need it, here are the [rules for SAPsim programs](https://SAPsim.readthedocs.io/en/latest/rules.html).

## Documentation

[https://SAPsim.readthedocs.io](https://SAPsim.readthedocs.io/en/latest/)
