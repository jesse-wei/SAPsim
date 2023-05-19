# SAPsim [![Python 3.9+ badge](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/) [![PyPI version badge](https://badge.fury.io/py/SAPsim.svg)](https://pypi.org/project/SAPsim/) [![tests GitHub action badge](https://github.com/jesse-wei/SAPsim/actions/workflows/tests.yml/badge.svg)](https://github.com/jesse-wei/SAPsim/actions/workflows/tests.yml) [![codecov badge](https://codecov.io/github/jesse-wei/SAPsim/branch/main/graph/badge.svg?token=RS7QI9QVKU)](https://codecov.io/github/jesse-wei/SAPsim) [![documentation badge](https://readthedocs.org/projects/sapsim/badge/?version=latest)](https://SAPsim.readthedocs.io/en/latest/)

Simulation of SAP (Simple-As-Possible computer) programs from COMP311 (Computer Organization) @ [UNC](https://unc.edu).

<p align="center">
    <img src="https://raw.githubusercontent.com/jesse-wei/SAPsim/main/docs/_static/SAPsim_demo.gif" alt="SAPsim demo">
</p>

## Install

`pip install SAPsim`

Your Python version needs to be 3.9+. Check with `python --version`.

If `python` doesn't work, try `python3`. If `pip` doesn't work, try `pip3`.

## Usage

Write a SAP program in the CSV file format shown below (templates are provided in COMP311's SAP assignment).

<p align="center">
    <img src="https://raw.githubusercontent.com/jesse-wei/SAPsim/main/docs/_static/ex1.jpg" alt="Screenshot of ex1.csv in Excel">
</p>
<p align="center">
    <a href="https://github.com/jesse-wei/SAPsim/blob/main/tests/public_prog/ex1.csv">ex1.csv</a>
</p>

You may edit the `.csv` file with any program (Microsoft Excel, Google Sheets, etc.).

To run the SAP program, use `run()`. **Note**: There is a debug (step) mode, as shown below.

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
...
```

If you want a blank template, use `create_template()`.

```py
>>> from SAPsim import create_template
>>> create_template()
template.csv successfully created.
```

## Settings

`change` lets you conveniently modify initial values in the SAP program without editing the CSV.

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

`table_format` lets you customize the appearance of the printed tables. [Options](https://github.com/astanin/python-tabulate#table-format).

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

Here's a list of [additional settings](https://SAPsim.readthedocs.io/en/latest/#additional-settings).

## Rules

It's easy to just mimic the [example programs](https://github.com/jesse-wei/SAPsim/tree/main/tests/public_prog), but if you need it, here's the list of [rules for SAPsim programs](https://SAPsim.readthedocs.io/en/latest/rules.html).

## SAP instruction set

<p align="center">
    <img src="https://raw.githubusercontent.com/jesse-wei/SAPsim/main/docs/_static/sap_instruction_set.jpg" alt="SAP instruction set">
</p>

## Documentation

[https://SAPsim.readthedocs.io](https://SAPsim.readthedocs.io/en/latest/)
