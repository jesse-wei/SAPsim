# Rules

```{topic} Overview

These are the rules for SAPsim programs.
```

```{contents}
---
depth: 3
---
```

## Specifications

- All SAP programs fit in 16 addresses (0 to 15) because the program counter (`PC`) is 4-bit. [^technicality_pc]
- The initial state of a SAP program is ``{PC: 0, Register A: 0, Register B: 0, FlagC: 0, FlagZ: 0, Executing: 1}``. [^technicality]
- ``A`` and ``B`` registers are 8-bit by default. [^bits_in_registers] The bit patterns are always interpreted as unsigned integers by SAPsim.

  - If the registers are interpreted as unsigned ints, what would 0-1 be? What about 255+1? See this footnote for the answer. [^answer]

## General

- Everything in RAM is a byte. [^bytes] Therefore, instructions and data are both represented as a First Hexit and Second Hexit.

  - An instruction's First Hexit is its 2 or 3 letter Mnemonic. An instruction's Second Hexit is its Arg.

    - An instruction's Arg can be represented in base-10 or base-16.
    - For example, ``JC 15`` could also be written as ``JC F``.

  - All data must fit in a byte.

    - For example, 254 = ``0xFE`` is First Hexit ``F``, Second Hexit ``E``.
    - 10 = ``0x0A`` is First Hexit ``0``, Second Hexit ``A``. You may not omit the leading 0.

- Programs run until they ``HLT`` or until an Exception is raised. Infinite loops are possible, of course.

```{note}
These are the same rules a SAP computer implemented by hardware has to follow.

"This is a feature, not a bug"
```

## Allowed syntax

In the First Hexit column, these are allowed

* Two or three letter Mnemonic [^interpret]
* Hexit ``0`` to ``F``
* Double digit base-10 integer ``10`` to ``15`` representing a hexit

In the Second Hexit column, these are allowed

* Hexit ``0`` to ``F``
* Double-digit base-10 integer ``10`` to ``15`` representing a hexit

  * e.g. ``JC 15`` and ``JC F`` are both legal and represent the same instruction

[^technicality_pc]: Admittedly, this limitation doesn't have to exist in software. However, suppose there were an address 16 and you do ``LDA 16``. This instruction doesn't fit in a single byte, which would be an implementation issue.

[^technicality]: In the ALU lab, the initial value of FlagZ was 1, but it's initialized to 0 here.

[^bits_in_registers]: `run()` allows you to configure the number of bits in registers. You should never need to change this value, however. During autograding, ``NUM_BITS_IN_REGISTERS`` is always 8.

[^answer]: If interpreting 8-bit register values as unsigned integers, 0-1=255, and 255+1=0. In both cases, the numbers "wrap around". If this doesn't quite click, play with the ALU with **4-bit** registers that you implemented! It follows all the same rules; just interpret the registers' bit patterns as unsigned integers for these examples.

[^bytes]: Specifically, RAM is represented as a `dict[int, int]`, where the keys are memory addresses 0-15 and the values are integers ranging from 0 to 255. SAPsim cannot tell at compile-time if a row in your program is "instruction" or "data". During parsing, any textual mnemonics you write will first be converted to an opcode, if possible, so that the information can be stored in a `dict[int, int]`. At runtime, SAPsim interprets the byte based on context (i.e., are we executing that byte or reading the value of that byte using `LDA`?). The only exception to this rule occurs when the byte has an invalid opcode (byte ranging from ``0x90`` to ``0xDF``) so definitely can't be an instruction.

[^interpret]: For an instruction's First Hexit field, you could technically write the Mnemonic as an opcode/hexit. SAPsim converts Mnemonics in the First Hexit column to opcodes anyway.
