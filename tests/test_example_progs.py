"""Test example programs.
This code should be the same (or mostly the same, in case it's updated) as the code that autogrades Lab 4.
If you have any questions about RESERVED/RETURN VALUE, they can be answered by reading through this.
If you don't know the test cases your program is failing, you can easily repurpose this code to find out."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from typing import Union, Any
from SAPsim import run_and_return_state


def test_ex1():
    """Test ex1.csv.
    RESERVED:
        14: Input 0 to 255
    RETURN VALUE:
        15: 1 if X == 3 else 0
    """
    for num in range(256):
        try:
            state: dict[str, Any] = run_and_return_state(
                "tests/public_prog/ex1.csv", change={14: num}
            )
        except Exception:
            # Note when an Exception occurs, the rest of the tests don't run.
            break
        # Autograder has a tests_passed variable and adds 1 to it if the RETURN VALUE is correct.
        assert int(num == 3) == state["RAM"][15]
    # score = tests_passed / total_tests


def test_ex2():
    """Test ex2.csv.
    RESERVED:
        15: Input 0 to 255
    RETURN VALUE:
        Register A: See ex2_rv() function
    """
    for num in range(256):
        try:
            state: dict[str, Any] = run_and_return_state(
                "tests/public_prog/ex2.csv", change={15: num}
            )
        except Exception:
            # Note when an Exception occurs, the rest of the tests don't run.
            break
        # The autograder has a tests_passed variable and adds 1 to it if the RETURN VALUE is correct.
        assert ex2_rv(num) == state["A"]
    # score = tests_passed / total_tests


def ex2_rv(X):
    """Helper function for testing ex2.csv. Just the example pseudocode to be replicated.
    Can make it not use a loop and instead use an if < 16 and then a mod operation but I don't have time for that.
    """
    while X >= 31:
        X = X - 3
    return X
