.. _rules:

#####
Rules
#####

.. topic:: Overview

    These are the rules that SAPsim programs must follow.

.. contents::
    :depth: 3

Specifications
##############

- All SAP programs fit in 16 addresses (0 to 15) because the program counter (``PC``) is 4-bit.
- Initial values are ``{PC: 0, Register A: 0, Register B: 0, FlagC: 0, FlagZ: 0, Executing: 1}``. [#technicality]_
- ``A`` and ``B`` registers are unsigned and 8-bit by default.

  - With 8-bit unsigned registers, what would 0-1 be? What about 255+1? See this footnote for the answer. [#answer]_

General
#######

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
SAPsim can't distinguish between instructions and data (most of the time). [#bytes]_

Disallowed syntax
#################

If you follow the templates and example programs, you won't run into any problems.
But if something goes wrong, an exception will occur, and there'll be a descriptive error message.

The full list of Exceptions is in `exceptions.py <SAPsim.utils.html#module-SAPsim.utils.exceptions>`_.

.. rubric:: Footnotes

.. [#technicality] In the ALU lab, the initial value of FlagZ was 1, but it's initialized to 0 here.

.. [#answer] With 8-bit unsigned registers, 0-1=255, and 255+1=0. In both cases, the numbers "wrap around". If this doesn't quite click, play with the ALU with **4-bit** registers that you implemented! It follows all the same rules; just think of its registers as unsigned for these examples.

.. [#bytes] In SAPsim, every value in RAM is a byte. See the `definition of RAM <SAPsim.utils.html#SAPsim.utils.globs.RAM>`_. Therefore, SAPsim has no concept of "instruction" or "data." It interprets the byte based on context (i.e., are we executing that byte or reading the value of that byte?). The only exception to this rule occurs when the byte has an invalid opcode (byte ranging from ``0x90`` to ``0xDF``) so can't be an instruction.
