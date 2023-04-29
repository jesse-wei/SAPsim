"""Test the run function in SAPsim.__init__.py.

Tests run(..., debug=True), which blocks on input,
with run(..., non_blocking=True), which doesn't block on input (by not calling ``input()``)
but is otherwise identical.

Remove the TEMP_FILE_PATH in the final test."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import sys
import os

from pathlib import Path
from SAPsim import run

TEMP_FILE_PATH: Path = Path("tests/out.txt")
ORIG_STDIN = sys.stdin
ORIG_STDOUT = sys.stdout

EX1_DEBUG_NUM_TIMES_PRESS_ENTER: int = 6
EX2_DEBUG_NUM_TIMES_PRESS_ENTER: int = 23


def test_run_ex1() -> None:
    """Test ex1.csv"""
    f = open(TEMP_FILE_PATH, "w")
    sys.stdout = f
    # Use plain table_fmt to avoid special characters that aren't the same on Ubuntu and Windows (unit tests)
    run("tests/public_prog/ex1.csv", table_format="plain")
    f.close()

    f2 = open(TEMP_FILE_PATH, "r")
    expected = open("tests/data/public_prog/ex1_plain.txt", "r")

    assert f2.readlines() == expected.readlines()

    f2.close()
    expected.close()


def test_run_ex2() -> None:
    f = open(TEMP_FILE_PATH, "w")
    sys.stdout = f
    # Use plain table_fmt to avoid special characters that aren't the same on Ubuntu and Windows (unit tests)
    run("tests/public_prog/ex2.csv", table_format="plain")
    f.close()

    f2 = open(TEMP_FILE_PATH, "r")
    expected = open("tests/data/public_prog/ex2_plain.txt", "r")

    assert f2.readlines() == expected.readlines()

    f2.close()
    expected.close()


def test_run_debug_ex1() -> None:
    f = open(TEMP_FILE_PATH, "w")
    sys.stdout = f
    # Use plain table_fmt to avoid special characters that aren't the same on Ubuntu and Windows (unit tests)
    run("tests/public_prog/ex1.csv", table_format="plain", non_blocking=True)
    f.close()

    f2 = open(TEMP_FILE_PATH, "r")
    expected = open("tests/data/public_prog/ex1_debug_plain.txt", "r")

    assert f2.readlines() == expected.readlines()

    f2.close()
    expected.close()


def test_run_debug_ex2() -> None:
    f = open(TEMP_FILE_PATH, "w")
    sys.stdout = f
    # Use plain table_fmt to avoid special characters that aren't the same on Ubuntu and Windows (unit tests)
    run("tests/public_prog/ex2.csv", table_format="plain", non_blocking=True)
    f.close()

    f2 = open(TEMP_FILE_PATH, "r")
    expected = open("tests/data/public_prog/ex2_debug_plain.txt", "r")

    assert f2.readlines() == expected.readlines()

    f2.close()
    expected.close()


def test_cleanup() -> None:
    """Not a real test, just clean up"""
    sys.stdin = ORIG_STDIN
    sys.stdout = ORIG_STDOUT
    os.remove(TEMP_FILE_PATH)
