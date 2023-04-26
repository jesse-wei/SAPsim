"""Test the run function in SAPsim.__init__.py.

Ideally, would like to test run(..., debug=True) but can't really send keyboard input, might require threading.

Remove the TEMP_FILE_PATH in the final test."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import sys
import os

# from pynput.keyboard import Key, Controller
# import time
# import threading
from pathlib import Path
from SAPsim import run

TEMP_FILE_PATH: Path = Path("tests/out.txt")
ORIG_STDIN = sys.stdin
ORIG_STDOUT = sys.stdout
# KEYBOARD: Controller = Controller()

EX1_DEBUG_NUM_TIMES_PRESS_ENTER: int = 6
EX2_DEBUG_NUM_TIMES_PRESS_ENTER: int = 23


# def thread_press_enter(num_times: int, first_time = True) -> None:
#     """Press enter a given number of times."""
#     if first_time:
#         # Give time for the next line of the program to run
#         # Before pressing key
#         time.sleep(1)
#     for _ in range(num_times):
#         # sys.stdin.write("\n")
#         KEYBOARD.press(Key.enter)
#         KEYBOARD.release(Key.enter)
#         time.sleep(0.1)


def test_run_ex1() -> None:
    """Test ex1.csv"""
    f = open(TEMP_FILE_PATH, "w")
    sys.stdout = f
    # Use plain table_fmt to avoid special characters that aren't the same on Ubuntu and Windows (unit tests)
    run("tests/public_prog/ex1.csv", table_fmt="plain")
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
    run("tests/public_prog/ex2.csv", table_fmt="plain")
    f.close()

    f2 = open(TEMP_FILE_PATH, "r")
    expected = open("tests/data/public_prog/ex2_plain.txt", "r")

    assert f2.readlines() == expected.readlines()

    f2.close()
    expected.close()


# def test_run_debug_ex1() -> None:
#     f = open(TEMP_FILE_PATH, "w")
#     sys.stdout = f
#     # Use plain table_fmt to avoid special characters that aren't the same on Ubuntu and Windows (unit tests)
#     t = threading.Thread(target=thread_press_enter, args=(EX1_DEBUG_NUM_TIMES_PRESS_ENTER,))
#     t.start()
#     run("tests/public_prog/ex2.csv", debug=True, table_fmt="plain")
#     f.close()

#     f2 = open(TEMP_FILE_PATH, "r")
#     expected = open("tests/data/public_prog/ex2_plain.txt", "r")

#     assert f2.readlines() == expected.readlines()

#     f2.close()
#     expected.close()


def test_cleanup() -> None:
    """Not a real test, just clean up"""
    sys.stdin = ORIG_STDIN
    sys.stdout = ORIG_STDOUT
    os.remove(TEMP_FILE_PATH)
