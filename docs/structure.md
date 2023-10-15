# Project structure

```{topic} Overview
This page describes the high-level structure of the codebase. Most descriptions are paraphrased from the docstrings of the files.
```

```{contents}
---
depth: 2
---
```

## Top-level

```text
SAPsim
├── LICENSE
├── README.md
├── SAPsim                  Source code
├── docs                    Documentation
├── pyproject.toml          Python project configuration
├── requirements.txt        Developer dependencies (e.g., testing, formatting, documentation), contains all functional dependencies from setup.py
├── setup.py                Python package configuration, lists all necessary dependencies installed during pip installation
├── testdist                Script for testing package before PyPI release
├── template.csv            Blank SAPsim CSV template
├── tests                   Tests
└── tox.ini                 Tox config file; tox is used for running tests in different OS and Python environments
```

## Source code

```text
SAPsim
├── __init__.py             Defines user-importable functions run, run_and_return_state, and create_template
└── utils
    ├── __init__.py
    ├── exceptions.py       Custom exceptions
    ├── execute.py          Execute instructions in RAM
    ├── global_vars.py      Global variables (variables that change throughout execution and constants)
    ├── helpers.py          Misc. helper functions
    ├── instructions.py     SAP instruction implementation
    └── parser.py           Parses a SAP program in SAPsim CSV format into global_vars.RAM
```

## Tree

These diagrams were generated using [tree](https://en.wikipedia.org/wiki/Tree_(command)). Irrelevant files were removed.
