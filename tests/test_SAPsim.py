"""Test the importable functions in SAPsim.__init__.py.

Tests run(..., debug=True), which blocks on input,
with run(..., non_blocking=True), which doesn't block on input (by not calling ``input()``)
but is otherwise identical.

Remove the TEMP_FILE_PATH in the final test."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import sys
import subprocess
from typing import Any, Union
import pytest

from SAPsim import run, create_template
import SAPsim.utils.parser as parser
import SAPsim.utils.exceptions as exceptions

STDOUT_FILE: str = "tests/stdout"
STDERR_FILE: str = "tests/stderr"
ORIG_STDOUT = sys.stdout
ORIG_STDERR = sys.stderr


def test_run_ex1() -> None:
    """Test ex1.csv"""
    write_run_stdout_stderr("tests/public_prog/ex1.csv", table_format="plain")
    assert file_match(STDOUT_FILE, "tests/data/public_prog/ex1_plain.txt")


def test_run_ex2() -> None:
    write_run_stdout_stderr("tests/public_prog/ex2.csv", table_format="plain")
    assert file_match(STDOUT_FILE, "tests/data/public_prog/ex2_plain.txt")


def test_run_debug_ex1() -> None:
    write_run_stdout_stderr(
        "tests/public_prog/ex1.csv", table_format="plain", non_blocking=True
    )
    assert file_match(STDOUT_FILE, "tests/data/public_prog/ex1_debug_plain.txt")


def test_run_debug_ex2() -> None:
    write_run_stdout_stderr(
        "tests/public_prog/ex2.csv", table_format="plain", non_blocking=True
    )
    assert file_match(STDOUT_FILE, "tests/data/public_prog/ex2_debug_plain.txt")


def test_run_change_ex1() -> None:
    """Test ``change`` kwarg of ``run()``."""
    state_eq: dict[str, Any] = run(
        "tests/public_prog/ex1.csv", return_state=True, change={13: 4, 14: 4}
    )
    state_neq: dict[str, Any] = run(
        "tests/public_prog/ex1.csv", return_state=True, change={13: 5, 14: 4}
    )
    assert state_eq["RAM"][15] == 1
    assert state_neq["RAM"][15] == 0


def test_run_change_maps_unmapped_addr() -> None:
    """Test that ``change`` kwarg of ``run()`` will map an unmapped address but print a warning
    to stderr."""
    state: dict[str, Any] = write_run_stdout_stderr(
        "tests/public_prog/ex1.csv", return_state=True, change={9: 1, 10: 2}
    )
    assert state["RAM"][9] == 1
    assert state["RAM"][10] == 2
    with open(STDERR_FILE, "r") as f:
        assert (
            f.read()
            == f"WARNING: You attempted to change the following address(es) not mapped in the CSV: 9, 10.\nThis is likely unintentional, but they are now mapped, and the program will continue.\n"
        )


def test_run_change_input_validation() -> None:
    """Test that ``change`` kwarg of ``run()`` will not map negative addrs and
    addrs > ``MAX_PC``."""
    with pytest.raises(exceptions.ChangeAddressNegative):
        run("tests/public_prog/ex1.csv", change={-1: 1})
    with pytest.raises(exceptions.ChangeAddressGreaterThan15):
        run("tests/public_prog/ex1.csv", change={16: 1})
    with pytest.raises(exceptions.ChangeValueInvalid):
        run("tests/public_prog/ex1.csv", change={0: -1})
    with pytest.raises(exceptions.ChangeValueInvalid):
        run("tests/public_prog/ex1.csv", change={0: 256})


def test_create_template() -> None:
    create_template(STDOUT_FILE)
    assert file_match(STDOUT_FILE, "template.csv")
    # Test no Exception thrown
    parser.parse_csv(STDOUT_FILE)


def write_run_stdout_stderr(prog_path: str, **kwargs) -> Union[None, dict[str, Any]]:
    """Write the ``stdout`` and ``stderr`` outputs of ``run(prog_path, **kwargs)`` to
    ``STDOUT_FILE`` and ``STDERR_FILE``, respectively..

    :param prog_path: Path to program to run
    :type prog_path: str
    :param **kwargs: Keyword arguments to pass to ``run()``
    :type **kwargs: dict"""
    state: Union[None, dict[str, Any]]
    with open(STDOUT_FILE, "w") as stdout:
        with open(STDERR_FILE, "w") as stderr:
            sys.stdout = stdout
            sys.stderr = stderr
            state = run(prog_path, **kwargs)
            sys.stdout = ORIG_STDOUT
            sys.stderr = ORIG_STDERR
    return state


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
