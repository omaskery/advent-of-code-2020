from dataclasses import dataclass
from typing import List
import enum


@enum.unique
class Opcode(enum.Enum):
    """distinguishes which operation an instruction should perform"""

    Accumulate = enum.auto()
    Jump = enum.auto()
    NoOperation = enum.auto()


@dataclass
class Instruction:
    """information needed to perform a single operation"""

    opcode: Opcode
    argument: int


class CPU:
    """processor of the handheld game console"""

    def __init__(self):
        """constructor that initialises the CPU object upon creation"""

        # the accumulator starts at 0
        self.accumulator = 0
        # we'll execute the first instruction in memory first
        self.instruction_pointer = 0
        # the computer has a program in memory, though it starts uninitialised
        self.program_memory: List[Instruction] = []

    def set_program_memory(self, program: List[Instruction]):
        """initialise the processor's program memory"""

        self.program_memory = program

    def execute_instruction(self):
        """executes a single instruction"""

        # fetch the next instruction to execute, note that if you run off the end of the program you cycle
        # around to the start
        instruction = self.program_memory[self.instruction_pointer % len(self.program_memory)]
        # most instructions simply move onto the next instruction upon completion, so let's default to
        # considering the next instruction as the one we'll do next, individual operations can override this
        next_instruction_pointer = self.instruction_pointer + 1

        if instruction.opcode == Opcode.NoOperation:
            # nop operations do nothing! :)
            pass
        elif instruction.opcode == Opcode.Jump:
            # jmp operations override the next instruction to execute
            next_instruction_pointer = self.instruction_pointer + instruction.argument
        elif instruction.opcode == Opcode.Accumulate:
            # acc operations add their argument to the accumulator
            self.accumulator += instruction.argument
        else:
            raise Exception(f"failed to execute unknown instruction {instruction.opcode} at {self.instruction_pointer}")

        # record which instruction to record next
        self.instruction_pointer = next_instruction_pointer


def load_instruction(line: str) -> Instruction:
    """decode an instruction from a line of text from the input"""

    # start by splitting the line by whitespace, to separate the opcode and argument
    parts = line.split()
    if len(parts) != 2:
        raise Exception(f"invalid instruction '{line}' expected two tokens, an opcode and argument")

    # we've confirmed that we split it into two parts, so let's give those parts nicer names to work with
    opcode_mneumonic, argument = parts

    # use a dictionary to map the text mneumonics for instructions to an enumeration of constant values
    opcode_lookup = {
        'nop': Opcode.NoOperation,
        'acc': Opcode.Accumulate,
        'jmp': Opcode.Jump,
    }

    if opcode_mneumonic not in opcode_lookup:
        raise Exception(f"unknown instruction '{opcode_mneumonic}'")

    # return the finalised instruction
    return Instruction(
        opcode=opcode_lookup[opcode_mneumonic],
        argument=int(argument),
    )


def main():
    # load the boot program from the input file
    with open('input/day8.txt') as f:
        boot_program = [
            load_instruction(line)
            for line in f
        ]

    # initialise the CPU
    cpu = CPU()
    # load the boot program into the processor
    cpu.set_program_memory(boot_program)

    # keep track of which instructions we've executed
    instructions_executed = set()
    # keep running instructions, until you try to run one for a second time
    while cpu.instruction_pointer not in instructions_executed:
        # record the instruction we're about to execute
        instructions_executed.add(cpu.instruction_pointer)

        cpu.execute_instruction()

    print(f"just before the program executes an instruction for the second time, the accumulator is: {cpu.accumulator}")


if __name__ == '__main__':
    main()
