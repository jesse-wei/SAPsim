"""Test exception handling."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import src.utils.globs as globs
from src.utils.execute import execute_full_speed, execute_next
from src.utils.helpers import check_state, check_state_all, print_RAM, print_info
from src.utils.exceptions import *
from src.utils.helpers import setup_4bit, setup_8bit, reset_globals
from src.utils import parser
import pytest

def test_16MappedAddresses():
    setup_8bit()
    parser.parse_csv('tests/malformed_csv/16_mapped_addresses.csv')

def test_17MappedAddresses():
    setup_8bit()
    with pytest.raises(MoreThan16MappedAddresses):
        parser.parse_csv('tests/malformed_csv/17_mapped_addresses.csv')

