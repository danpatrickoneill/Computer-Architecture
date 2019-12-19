"""CPU functionality."""

import sys

LDI = '10000010'
PRN = '01000111'
HLT = '00000001'
MUL = '10100010'
PUSH = '01000101'
POP = '01000110'

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 64
        self.reg = [0] * 8
        self.sp = 48
        self.ir = None
        self.ie = None
        self.fl = None

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = []

        with open(filename) as p:
            for line in p:                    
                # print(line)
                if line[0] == '#' or line[0] == '\n':
                    # print("Skipping commented or blank line...")
                    continue
                else:
                    program.append(line[:8])

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_write(self, address, value):
        self.ram[address] = value

    def ram_read(self, address):
        return self.ram[address]

    def run(self):
        """Run the CPU."""
        halted = False
        ir = self.pc
        while not halted:
            instruction = self.ram_read(ir)
            # print(instruction)
            # self.trace()
            if instruction == LDI:
                # print("Loading immediate...")
                operand_a = int(self.ram_read(ir + 1), 2)
                operand_b = int(self.ram_read(ir + 2), 2)
                self.reg[operand_a] = operand_b
                ir += 3
            elif instruction == PRN:
                # print("Printing...")
                target_reg = int(self.ram_read(ir + 1), 2)
                print(self.reg[target_reg])
                ir += 2
            elif instruction == MUL:
                # print("Multiplying...")
                target_reg_a = int(self.ram_read(ir + 1), 2)
                target_reg_b = int(self.ram_read(ir + 2), 2)
                product = self.reg[target_reg_a] * self.reg[target_reg_b]
                self.reg[target_reg_a] = product
                ir += 3
            elif instruction == PUSH:
                # print("Pushing...")
                target_reg = int(self.ram_read(ir + 1), 2)
                self.sp -= 1
                self.ram_write(self.sp, self.reg[target_reg])
                ir += 2
            elif instruction == POP:
                # print("Popping...")
                target_reg = int(self.ram_read(ir + 1), 2)
                # print(f'Target register: {target_reg}')
                value = self.ram_read(self.sp)
                self.sp += 1
                self.reg[target_reg] = value
                ir += 2
            elif instruction == HLT:
                # print("Halting!")
                halted = True
            else:
                print(f"Unrecognized instruction: {instruction} at counter: {ir}. Halting program...")
                ir += 1
                halted = True