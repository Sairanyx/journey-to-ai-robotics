# Lecture 1 - Introduction to Embedded Systems

## What is an Embedded System?
An embedded system is a:
- Task-specific system
- Interacts with environment/users
- Controls physical processes
- Often real-time
- Embedded inside a larger system

## Examples
- Domestic appliances
- Smart devices
- Consumer electronics
- Automation systems

## Embedded System Components
- Microcontroller
- Memory
- Peripherals
- Sensors & actuators

## Key Features
- Limited resources (CPU, memory, energy)
- Time-critical behavior
- Safety-critical applications
- Interactive & control-oriented

## Challenge
> Achieve high performance with low resources

## C Programming?
- Close to hardware
- High performance & low energy usage
- Efficient memory control
- Portable across systems
- No overhead (no garbage collection)

## Computing Stack

- Problem → Algorithm → Programming Language → Compiler → OS → Hardware

## Structure of a C Program
- Documentation (comments)
- Libraries (`#include`)
- Definitions (`#define`)
- Global variables
- `main()` function (entry point)
- Code logic

## Program Execution Flow
1. Preprocessing
2. Compilation
3. Assembly
4. Linking
5. Executable runs

- example.c
- example.i
- example.s
- example.o
- example.exe

## Example Commands
```bash
gcc file.c -o file     # compile and link
gcc -E file.c         # preprocess only
gcc -S file.c         # compile to assembly
gcc -c file.c         # create object file

# Lecture 2 - Basic Syntax of C and practise

