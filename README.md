# SAPsim

![Test badge](https://github.com/jesse-wei/SAPsim/actions/workflows/tests.yml/badge.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Python](https://img.shields.io/badge/python-3670A0?style=plastic&logo=python&logoColor=ffdd54)

> Simulation of [SAP (Simple As Possible) computer](https://jessewei.dev/img/sap.jpg) programs from COMP311 (Computer Organization) @ [UNC](https://unc.edu).

<p align="center">
    <img src="https://jessewei.dev/img/SAPsim_demo.gif" alt="SAPsim demo">
</p>

## Install

Your Python version needs to be 3.9+. Check with `python --version` or `python3 --version`, if `python` doesn't work.

Next, install SAPsim.

```sh
pip install SAPsim
```

If `pip` doesn't work, try `pip3`.

## Usage

Write a SAP program in the format shown in [ex2.csv](https://github.com/jesse-wei/SAPsim/blob/main/tests/public_prog/ex2.csv). See [template.csv](https://github.com/jesse-wei/SAPsim/blob/main/template.csv) for a blank template. You may edit the `.csv` files in Microsoft Excel.

Open a Python terminal. You'll pass the path to your SAP program as an argument.

```py
from SAPsim import run

run("path/to/your/SAP/program.csv")                 # run at full speed (default)
run("path/to/your/SAP/program.csv", debug=True)     # run in debug (step) mode
```

Here's a list of [additional settings](https://SAPsim.readthedocs.io/en/latest/#settings) (e.g., table format).

## Rules

It's easy to just mimic the example programs [above](#usage).
But if you need it, here's the list of [rules for SAPsim programs](https://SAPsim.readthedocs.io/en/latest/rules.html).

## SAP instruction set

![SAP instruction set](https://user-images.githubusercontent.com/55986131/220041985-da3060d2-18c3-4158-8d30-a5d88e08acc4.png)

## Documentation

[https://SAPsim.readthedocs.io](https://SAPsim.readthedocs.io/en/latest/)
