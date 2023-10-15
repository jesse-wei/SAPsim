# Example SAP programs

`ex1.csv` and `ex2.csv` are commented example programs that implement the pseudocode below.

You can, of course, run them with any input (0 to 255) by modifying what's at the address RESERVED for input.

## [ex1](ex1.csv)

```c
uint8_t X = input()     // input() is a RESERVED data value (0 to 255) at address 14
if (X == 3)
    return 1;           // Return at address 15, then halt
else
    return 0;           // Return at address 15, then halt
```

## [ex2](ex2.csv)

```c
uint8_t X = input()     // input() is a RESERVED data value (0 to 255) at address 15
while (X >= 31)
    X = X - 3;
return X;               // Load into Register A, then halt
```
