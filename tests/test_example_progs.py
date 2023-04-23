"""Test example programs.
This code should be the same (or mostly the same, in case it's updated) as the code that autogrades Lab 4.
If you have any questions about RESERVED/RETURN VALUE, they can be answered by reading through this.
If you don't know the test cases your program is failing, you can very easily write a function to check it yourself. It'd probably be exactly the same as what I wrote.
"""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from SAPsim.utils import globs
from SAPsim.utils import parser
from SAPsim.utils.execute import execute_full_speed
from SAPsim.utils.helpers import setup_8bit


def clone_dict(dict):
    """Returns a deep clone of `dict`. Used to clone `RAM`."""
    rv = {}
    for key in dict:
        rv[key] = dict[key]
    return rv


def test_ex1():
    """Test ex1.csv.
    RESERVED:
        14: Input 0 to 255
    RETURN VALUE:
        15: 1 if x == 3 else 0
    """
    setup_8bit()
    parser.parse_csv("tests/public_prog/ex1.csv")
    # Clone student's program
    ram_copy = clone_dict(globs.RAM)
    for num in range(256):
        setup_8bit()
        globs.RAM = clone_dict(ram_copy)
        # Overwrite RESERVED address with test input
        globs.RAM[14] = num
        # We've chosen not to overwrite RETURN VALUE address to a wrong value before execution, which we could have done to prevent hardcoding
        # ex1.csv doesn't take advantage of this
        # Is there a way to take advantage of this in your flags.csv program?
        # globs.RAM[15] = 0x42
        try:
            execute_full_speed()
        except Exception:
            # Note when an Exception occurs, the rest of the tests don't run. The break is for performance reasons.
            break
        # The autograder has a tests_passed variable and adds 1 to it if the RETURN VALUE is correct
        assert int(num == 3) == globs.RAM[15]

    # score = tests_passed / total_tests


def test_ex2():
    """Test ex2.csv.
    RESERVED:
        15: Input 0 to 255
    RETURN VALUE:
        Register A: See ex2_rv() function
    """
    setup_8bit()
    parser.parse_csv("tests/public_prog/ex2.csv")
    # Clone student's program
    ram_copy = clone_dict(globs.RAM)
    for num in range(256):
        setup_8bit()
        globs.RAM = clone_dict(ram_copy)
        # Overwrite RESERVED address with test input
        globs.RAM[15] = num
        try:
            execute_full_speed()
        except Exception:
            # Note when an Exception occurs, the rest of the tests don't run. The break is for performance reasons.
            break
        # The autograder has a tests_passed variable and adds 1 to it if the RETURN VALUE is correct
        assert ex2_rv(num) == globs.A

    # score = tests_passed / total_tests


def ex2_rv(X):
    """Helper function for testing ex2.csv. Just the example pseudocode to be replicated.
    Can make it not use a loop and instead use an if < 16 and then a mod operation but I don't have time for that.
    """
    while X >= 31:
        X = X - 3
    return X
