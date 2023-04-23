"""Test exception handling."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import pytest
import SAPsim.utils.exceptions as exceptions
from SAPsim.utils.helpers import setup_4bit, setup_8bit
from SAPsim.utils import parser


def test_16MappedAddresses():
    setup_8bit()
    parser.parse_csv("tests/malformed_csv/16_mapped_addresses.csv")


def test_19MappedAddresses():
    setup_8bit()
    with pytest.raises(exceptions.MoreThan16MappedAddresses):
        parser.parse_csv("tests/malformed_csv/19_mapped_addresses.csv")
