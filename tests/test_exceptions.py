"""Test exception handling."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

from pathlib import Path
import pytest
import SAPsim.utils.exceptions as exceptions
from SAPsim.utils.helpers import setup_4bit, setup_8bit
from SAPsim.utils import parser, execute


def test_16MappedAddresses():
    setup_8bit()
    parser.parse_csv(Path("tests/malformed_csv/16_mapped_addresses.csv"))


def test_19MappedAddresses():
    setup_8bit()
    with pytest.raises(exceptions.MoreThan16MappedAddresses):
        parser.parse_csv(Path("tests/malformed_csv/19_mapped_addresses.csv"))


def test_DroppedOffBottom():
    setup_8bit()
    with pytest.raises(exceptions.DroppedOffBottom):
        execute.run("tests/malformed_csv/drop_off_bottom.csv")


def test_NoFirstHexit():
    setup_8bit()
    with pytest.raises(exceptions.NoFirstHexit):
        parser.parse_csv(Path("tests/malformed_csv/no_first_hexit_addr_15.csv"))


def test_DuplicateAddress():
    setup_8bit()
    with pytest.raises(exceptions.DuplicateAddress):
        parser.parse_csv(Path("tests/malformed_csv/dup_addr_0.csv"))


def test_first_hexit_greater_than_15():
    setup_8bit()
    with pytest.raises(exceptions.FirstHexitGreaterThan15):
        parser.parse_csv(Path("tests/malformed_csv/first_hexit_16_addr_0.csv"))


def test_NoSecondHexit():
    setup_8bit()
    with pytest.raises(exceptions.NoSecondHexit):
        parser.parse_csv(Path("tests/malformed_csv/no_second_hexit_addr_1.csv"))


def test_NegativeAddress():
    setup_8bit()
    with pytest.raises(exceptions.NegativeAddress):
        parser.parse_csv(Path("tests/malformed_csv/negative_addr_row_1.csv"))


def test_NoAddress():
    setup_8bit()
    with pytest.raises(exceptions.RowWithNoAddress):
        parser.parse_csv(Path("tests/malformed_csv/no_addr_row_16.csv"))


def test_NoAddress_2():
    setup_8bit()
    with pytest.raises(exceptions.RowWithNoAddress):
        parser.parse_csv(Path("tests/malformed_csv/blank_row_3.csv"))


def test_skipped_address_fine():
    setup_8bit()
    parser.parse_csv(
        Path("tests/malformed_csv/skipped_addr_1_should_drop_off_bottom.csv")
    )
