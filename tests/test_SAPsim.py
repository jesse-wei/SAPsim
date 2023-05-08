"""Test the importable functions in SAPsim.__init__.py.

Tests run(..., debug=True), which blocks on input,
with run(..., non_blocking=True), which doesn't block on input (by not calling ``input()``)
but is otherwise identical.

Remove the TEMP_FILE_PATH in the final test."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import sys
import os
import subprocess

from SAPsim import run, create_template
from SAPsim.utils import parser
from pathlib import Path

TEMP_FILE_PATH: str = "tests/out.txt"
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

    assert file_match(TEMP_FILE_PATH, "tests/data/public_prog/ex1_plain.txt")


def test_run_ex2() -> None:
    f = open(TEMP_FILE_PATH, "w")
    sys.stdout = f
    run("tests/public_prog/ex2.csv", table_format="plain")
    f.close()

    assert file_match(TEMP_FILE_PATH, "tests/data/public_prog/ex2_plain.txt")


def test_run_debug_ex1() -> None:
    f = open(TEMP_FILE_PATH, "w")
    sys.stdout = f
    run("tests/public_prog/ex1.csv", table_format="plain", non_blocking=True)
    f.close()

    assert file_match(TEMP_FILE_PATH, "tests/data/public_prog/ex1_debug_plain.txt")


def test_run_debug_ex2() -> None:
    f = open(TEMP_FILE_PATH, "w")
    sys.stdout = f
    run("tests/public_prog/ex2.csv", table_format="plain", non_blocking=True)
    f.close()
    assert file_match(TEMP_FILE_PATH, "tests/data/public_prog/ex2_debug_plain.txt")


def test_create_template() -> None:
    create_template(TEMP_FILE_PATH)
    assert file_match(TEMP_FILE_PATH, "template.csv")
    # Test no Exception thrown
    parser.parse_csv(TEMP_FILE_PATH)


def test_cleanup() -> None:
    """Not a real test, just clean up"""
    sys.stdin = ORIG_STDIN
    sys.stdout = ORIG_STDOUT
    os.remove(TEMP_FILE_PATH)


def file_match(file1: str, file2: str) -> bool:
    """Check if ``file1`` and ``file2`` are identical using the output of ``diff``.

    :param file1: Path to first file
    :type file1: str
    :param file2: Path to second file
    :type file2: str
    :return: True if identical, False otherwise
    :rtype: bool"""

    command: str = "diff -sbBd " + file1 + " " + file2
    proc = subprocess.run(command, capture_output=True, shell=True)
    return "identical" in proc.stdout.decode("utf-8")
