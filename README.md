[![tests GitHub action](https://github.com/jesse-wei/SAPsim/actions/workflows/tests.yml/badge.svg)](https://github.com/jesse-wei/SAPsim/actions/workflows/tests.yml)
[![documentation badge](https://readthedocs.org/projects/sapsim/badge/?version=latest)](https://SAPsim.readthedocs.io/en/latest/)

# SAPsim

Simulation of [SAP (Simple As Possible) computer](https://jessewei.dev/img/sap.jpg) programs from COMP311 (Computer Organization) @ [UNC](https://unc.edu).

<p align="center">
    <img src="https://raw.githubusercontent.com/jesse-wei/SAPsim/main/docs/_static/SAPsim_demo.gif" alt="SAPsim demo">
</p>

## Install

`pip install SAPsim`

Your Python version needs to be 3.9+. Check with `python --version`.

If `python` doesn't work, try `python3`. If `pip` doesn't work, try `pip3`.

## Usage

Write a SAP program in the CSV file format shown below.

<p align="center">
    <img src="https://raw.githubusercontent.com/jesse-wei/SAPsim/main/docs/_static/ex1.jpg" alt="Screenshot of ex1.csv in Excel">
</p>
<p align="center">
    <a href="https://github.com/jesse-wei/SAPsim/blob/main/tests/public_prog/ex1.csv">ex1.csv</a>
</p>

You may edit the `.csv` file with any program (Microsoft Excel, Google Sheets, etc.), as long as you preserve the `.csv` extension. For a blank template, see [template.csv](https://github.com/jesse-wei/SAPsim/blob/main/template.csv).

Open a Python terminal. Import SAPsim's `run()` function, and pass the path to your SAP program as an argument.

```py
>>> from SAPsim import run
>>> run("ex1.csv")                 # Run ex1.csv at full speed (default)
...
>>> run("ex1.csv", debug=True)     # Run ex1.csv in debug (step) mode
...
```

**Note**: There is a debug (step) mode, as shown above.

## Settings

Here's a list of [additional settings](https://SAPsim.readthedocs.io/en/latest/#settings) (e.g., printed table format).

## Rules

It's easy to just mimic the [example programs](https://github.com/jesse-wei/SAPsim/tree/main/tests/public_prog), but if you need it, here's the list of [rules for SAPsim programs](https://SAPsim.readthedocs.io/en/latest/rules.html).

## SAP instruction set

<p align="center">
    <img src="https://raw.githubusercontent.com/jesse-wei/SAPsim/main/docs/_static/sap_instruction_set.jpg" alt="SAP instruction set">
</p>

## Documentation

[https://SAPsim.readthedocs.io](https://SAPsim.readthedocs.io/en/latest/)
