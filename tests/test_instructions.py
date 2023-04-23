"""Test instructions."""

__author__ = "Jesse Wei <jesse@cs.unc.edu>"

import SAPsim.utils.globs as globs
from SAPsim.utils.execute import execute_full_speed, execute_next
from SAPsim.utils.helpers import check_state, check_state_all
from SAPsim.utils.exceptions import (
    DroppedOffBottom,
    ARegisterNotEnoughBits,
    LoadFromUnmappedAddress,
)
from SAPsim.utils.helpers import setup_4bit


def test_nop():
    setup_4bit()
    globs.RAM[0] = 0x00
    globs.RAM[1] = 0x01
    globs.RAM[2] = 0x02
    globs.RAM[4] = 0x0F
    try:
        execute_full_speed()
        assert False
    except DroppedOffBottom:
        pass
    check_state_all({0: 0x00, 1: 0x01, 2: 0x02, 4: 0x0F}, 5, 0, 0, False, False, False)


def test_lda():
    setup_4bit()
    globs.RAM[0] = 0x1F
    globs.RAM[1] = 0x1E
    globs.RAM[14] = 0x3
    globs.RAM[15] = 0x4
    execute_next()
    check_state_all({0: 0x1F, 1: 0x1E, 14: 0x3, 15: 0x4}, 1, 4, 0, False, False, True)
    execute_next()
    check_state_all({0: 0x1F, 1: 0x1E, 14: 0x3, 15: 0x4}, 2, 3, 0, False, False, True)


def test_lda_raises_ARegisterOverflow():
    setup_4bit()
    globs.RAM[0] = 0x1F
    globs.RAM[15] = 0x10
    try:
        execute_next()
        assert False
    except ARegisterNotEnoughBits:
        pass


def test_lda_from_unmapped_addr():
    setup_4bit()
    globs.RAM[0] = 0x1F
    try:
        execute_next()
        assert False
    except LoadFromUnmappedAddress:
        pass


def test_add():
    setup_4bit()
    globs.RAM[0] = 0x2F
    globs.RAM[1] = 0x2E
    globs.RAM[14] = 0xF
    globs.RAM[15] = 0xF
    execute_next()
    check_state(
        RAM={0: 0x2F, 1: 0x2E, 14: 0xF, 15: 0xF}, A=0xF, FLAG_C=False, FLAG_Z=False
    )
    execute_next()
    check_state(
        RAM={0: 0x2F, 1: 0x2E, 14: 0xF, 15: 0xF}, A=14, FLAG_C=True, Flag_Z=False
    )
    try:
        execute_full_speed()
        assert False
    except DroppedOffBottom:
        pass


def test_add_from_unmapped_addr():
    setup_4bit()
    globs.RAM[0] = 0x2F
    try:
        execute_next()
        assert False
    except LoadFromUnmappedAddress:
        pass


def test_sub():
    setup_4bit()
    globs.RAM[0] = 0x3F
    globs.RAM[1] = 0x3E
    globs.RAM[14] = 0x1
    globs.RAM[15] = 0xF
    execute_next()
    check_state(
        RAM={0: 0x3F, 1: 0x3E, 14: 0x1, 15: 0xF}, A=1, FLAG_C=False, FLAG_Z=False
    )
    execute_next()
    check_state(RAM={0: 0x3F, 1: 0x3E, 14: 0x1, 15: 0xF}, A=0, FLAG_C=True, FLAG_Z=True)


def test_sta_to_unmapped_addr():
    setup_4bit()
    globs.RAM[0] = 0x2F
    globs.RAM[1] = 0x4E
    globs.RAM[15] = 0xF
    execute_next()
    execute_next()
    check_state(
        RAM={0: 0x2F, 1: 0x4E, 0xE: 0xF, 0xF: 0xF},
        A=0xF,
        FLAG_C=False,
        FLAG_Z=False,
        PC=2,
        EXECUTING=True,
    )


def test_sta_overwrites_addr():
    setup_4bit()
    globs.RAM[0] = 0x2E
    globs.RAM[1] = 0x4F
    globs.RAM[14] = 2
    globs.RAM[15] = 1
    try:
        execute_full_speed()
        assert False
    except DroppedOffBottom:
        pass
    check_state_all({0: 0x2E, 1: 0x4F, 14: 2, 15: 2}, 16, 2, 2, False, False, False)


def test_ldi():
    setup_4bit()
    globs.RAM[0] = 0x59
    execute_next()
    check_state_all({0: 0x59}, 1, 9, 0, False, False, True)


def test_ldi_overwrites_A():
    setup_4bit()
    globs.A = 15
    globs.RAM[0] = 0x55
    execute_next()
    check_state_all({0: 0x55}, 1, 5, 0, False, False, True)


def test_ldi_doesnt_modify_flags():
    setup_4bit()
    globs.RAM[0] = 0x5A
    globs.FLAG_C = True
    globs.FLAG_Z = True
    execute_next()
    check_state_all({0: 0x5A}, 1, 0xA, 0, True, True, True)


def test_jmp():
    setup_4bit()
    globs.RAM[0] = 0x67
    execute_next()
    check_state_all({0: 0x67}, 7, 0, 0, False, False, True)


def test_jmp_executes_instruction():
    setup_4bit()
    globs.RAM[0] = 0x64
    globs.RAM[4] = 0x55
    globs.RAM[5] = 0x47
    execute_next()
    check_state_all({0: 0x64, 4: 0x55, 5: 0x47}, 4, 0, 0, False, False, True)
    execute_next()
    check_state_all({0: 0x64, 4: 0x55, 5: 0x47}, 5, 5, 0, False, False, True)
    execute_next()
    check_state_all({0: 0x64, 4: 0x55, 5: 0x47, 7: 5}, 6, 5, 0, False, False, True)
    execute_next()
    execute_next()
    try:
        execute_next()
        assert False
    except DroppedOffBottom:
        pass


def test_hlt():
    setup_4bit()
    globs.RAM[0] = 0xFF
    globs.RAM[15] = 0x10
    execute_next()
    check_state_all({0: 0xFF, 15: 0x10}, 0, 0, 0, False, False, False)
    for i in range(100):
        execute_next()
    check_state_all({0: 0xFF, 15: 0x10}, 0, 0, 0, False, False, False)
    for i in range(1000):
        execute_full_speed()
    check_state_all({0: 0xFF, 15: 0x10}, 0, 0, 0, False, False, False)
