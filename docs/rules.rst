.. _rules:

#####
Rules
#####

.. topic:: Overview

    These are the rules that SAPsim programs must follow.

.. contents::
    :depth: 3

General
#######

- All SAP programs fit in 16 addresses (0 to 15) because the program counter (``PC``) is 4-bit.
- Initial values are ``{PC: 0, Register A: 0, Register B: 0, FlagC: 0, FlagZ: 0, Executing: 1}``.
- ``A`` and ``B`` registers are unsigned and 8-bit by default. Number of bits is configurable.
- Instructions and data are all bytes. [#bytes]_

  - An instruction is a Mnemonic representing an Opcode (4-bit) and an Arg (4-bit).

    - For an instruction, the Arg can be represented in base-10 or base-16.
    - For example, ``JC 15`` could also be written as ``JC F``.

  - All data must fit in a byte. Specifically, the Mnemonic is a hexit, and the Arg is a hexit.

    - For example, 254 = ``0xFE`` is Mnemonic ``F``, Arg ``E``.
    - 10 = ``0x0A`` is Mnemonic ``0``, Arg ``A``. You may not omit the leading 0.

- Programs run until they ``HLT`` or until an Exception is raised. Infinite loops are possible, of course.

.. note::

    These are the same rules a SAP computer implemented by hardware has to follow.

    "This is a feature, not a bug"

Allowed syntax
##############

In the Mnemonic column, these are allowed

* two or three letter Mnemonic (for an instruction)
* single-digit hexit ``0`` to ``F`` (for data)

In the Arg column, these are allowed

* single-digit hexit ``0`` to ``F`` (for instruction or data)
* double-digit base-10 integer ``10`` to ``15`` representing a hexit

  * e.g. ``JC 15`` and ``JC F`` are both legal and represent the same instruction

Technically, the Mnemonic column also accepts a hex or decimal number representing an opcode.
SAPsim can't distinguish between instructions and data. [#bytes]_

Disallowed syntax
#################

If you follow the templates and example programs, you won't run into any problems.

But if something goes wrong, an exception will occur, and there'll be a descriptive error message.

The full list of Exceptions is in `exceptions.py <SAPsim.utils.html#module-SAPsim.utils.exceptions>`_.

.. rubric:: Footnotes

.. [#bytes] In SAPsim, every value in RAM is a byte. See the `definition of RAM <SAPsim.utils.html#src.utils.globs.RAM>`_.
