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

- All SAP programs fit in 16 addresses (0 to 15) because the program counter (``PC``) is 4-bit. [#technicality_pc]_
- Initial values are ``{PC: 0, Register A: 0, Register B: 0, FlagC: 0, FlagZ: 0, Executing: 1}``. [#technicality]_
- ``A`` and ``B`` registers are unsigned and 8-bit by default.

  - With 8-bit unsigned registers, what would 0-1 be? What about 255+1? See this footnote for the answer. [#answer]_

General
#######

- Everything in RAM is a byte. [#bytes]_ Therefore, instructions and data are both represented as a First Hexit and Second Hexit.

  - An instruction's First Hexit is its 2 or 3 letter Mnemonic. An instruction's Second Hexit is its Arg.

    - For an instruction, the Arg can be represented in base-10 or base-16.
    - For example, ``JC 15`` could also be written as ``JC F``.

  - All data must fit in a byte.

    - For example, 254 = ``0xFE`` is First Hexit ``F``, Second Hexit ``E``.
    - 10 = ``0x0A`` is First Hexit ``0``, Second Hexit ``A``. You may not omit the leading 0.

- Programs run until they ``HLT`` or until an Exception is raised. Infinite loops are possible, of course.

.. note::

    These are the same rules a SAP computer implemented by hardware has to follow.

    "This is a feature, not a bug"

Allowed syntax
##############

In the First Hexit column, these are allowed

* Two or three letter Mnemonic [#interpret]_
* Hexit ``0`` to ``F``
* Double digit base-10 integer ``10`` to ``15`` representing a hexit

    * However, this shouldn't be necessary

In the Second Hexit column, these are allowed

* Hexit ``0`` to ``F``
* Double-digit base-10 integer ``10`` to ``15`` representing a hexit

  * e.g. ``JC 15`` and ``JC F`` are both legal and represent the same instruction

.. rubric:: Footnotes

.. [#technicality_pc] Admittedly, this limitation doesn't have to exist in software. However, suppose there were an address 16 and you do ``LDA 16``. This instruction doesn't fit in a single byte, which would be an implementation issue.

.. [#technicality] In the ALU lab, the initial value of FlagZ was 1, but it's initialized to 0 here.

.. [#answer] With 8-bit unsigned registers, 0-1=255, and 255+1=0. In both cases, the numbers "wrap around". If this doesn't quite click, play with the ALU with **4-bit** registers that you implemented! It follows all the same rules; just think of its registers as unsigned for these examples.

.. [#bytes] In SAPsim, every value in RAM is a byte. See the `definition of RAM <SAPsim.utils.html#SAPsim.utils.global_vars.RAM>`_. Therefore, SAPsim cannot tell if a row in your program is "instruction" or "data." At runtime, it interprets the byte based on context (i.e., are we executing that byte or reading the value of that byte?). The only exception to this rule occurs when the byte has an invalid opcode (byte ranging from ``0x90`` to ``0xDF``) so can't be an instruction.

.. [#interpret] For an instruction's First Hexit field, you could technically write the Mnemonic as an opcode. SAPsim converts Mnemonics in the First Hexit column to opcodes anyway.
