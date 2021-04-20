#
# s21-ApplePi.py  --  Simulator class for ApplePi.
#
# Authors: Ray Loerke, Mark Liffiton
#
from print_utils import print_val, print_mem, print_input, print_matrix

import random
import time

# Constants for this architecture
_NUMREG = 16      # number of registers in the register file
_REGSIZE = 16     # size (in bits) of each register)
_ADDRSIZE = 16    # size (in bits) of DMEM addresses
_NUMBUTTONS = 4   # Number of buttons (binary on/off) for input
_MATRIXSIZE = 10  # width and height of the pixel matrix output


class Simulator:
    def __init__(self):
        # CPU state:
        self.imem = [0]  # not affected by CPU reset, so only initialized here
        self.reset()

        # Simulator state (separate from the CPU itself):
        self.bin_filename = ""

    def load_bin(self, filename):
        # Load machine code from a file into instruction memory
        self.bin_filename = filename
        with open(filename, "r") as f:
            data = f.read()
        words = data.split()
        self.imem = [int(word, 16) for word in words]

        # Always reset on loading new code
        self.reset()

    def change_buttons(self, new_buttons):
        # Change the state of the simulated buttons
        # Parameter: new_buttons is a string, containing a 0 or 1 for each button
        #            e.g. "0110" for the first button not pressed, the second and
        #            third pressed, and the fourth not pressed.
        buttonvals = [int(c) for c in new_buttons]
        if len(buttonvals) != _NUMBUTTONS:
            raise Exception(
                f"Incorrect number of buttons.  Got {len(buttonvals)}, expected {_NUMBUTTONS}."
            )
        if max(buttonvals) > 1 or min(buttonvals) < 0:
            raise Exception(
                f"Invalid value for button.  Only allowed values are 0 and 1."
            )
        self.buttons = buttonvals

    def step_n(self, n):
        # Simulate n cycles of the CPU (see self.step()).
        for _ in range(n):
            self.step()

    def watch_n(self, n):
        # Simulate n cycles of the CPU, as in step_n(), but watch the
        # state of the CPU by printing after every 100th cycle.
        for i in range(n):
            self.step()
            if i % 100 == 0:
                print("[2J[H")  # clear the screen and return to home position
                self.print()
                time.sleep(0.05)

    def reset(self):
        # Reset the CPU state to just-powered-on, with everything but IMEM cleared
        self.PC = 0
        self.regfile = [0] * _NUMREG
        self.dmem = [0] * 2 ** _ADDRSIZE
        self.buttons = [0] * _NUMBUTTONS
        self.matrix = [([0] * _MATRIXSIZE) for _ in range(_MATRIXSIZE)]
        # Setting up the one register
        self.regfile[1] = 1

    def print(self):
        # Print the current state of all state (memory) elements of the CPU
        print_val(self.PC, "PC")
        print_mem(self.imem, "IMEM", val_width=16, highlight=self.PC)
        print_mem(self.regfile, "Regfile", label_all=True)
        print_mem(self.dmem, "DMEM", limit_to_modified=True)
        print_input(self.buttons, "Input")
        print_matrix(self.matrix, "Output")

    def step(self):
        # Simulate *one* cycle of the CPU (Fetch-Decode-Execute)
        # Basic outline:
        #  1) Fetch the current instruction (using imem and PC)
        #  2) Decode the instruction into its different fields
        #  3) Execute the instruction by updating the CPU state
        #     according to what the execution of that instruction
        #     would do.

        instruction = self.imem[self.PC]
        # PC is incremented after the instruction is fetched
        self.PC += 1

        op, reg1, reg2, imm, tgt = self.decode(instruction)
        self.execute(op, reg1, reg2, imm, tgt)

    def decode(self, instruction):
        # The instruction passed to the function is separated into its various fields based on the instruction type
        # These are the op codes sorted into their instruction types
        # R-Format = 0, 1, 3, 4, 6, 9
        # I-Format = 2, 7, 8, 10
        # J-Format = 5
        op_mask = (0b1111 << 12)
        op = (instruction & op_mask) >> 12

        if op == 5:
            # For J-Format instructions only the op code and target need to be extracted
            tgt_mask = 0b111111111111
            tgt = instruction & tgt_mask
            # Fields not relevant to the instruction type are set to None
            reg1 = None
            reg2 = None
            imm = None
            # And each field of the instruction is returned
            return op, reg1, reg2, imm, tgt

        elif (op == 2) or (op == 7) or (op == 8) or (op == 10):
            # For I-Format instructions the op code, register 1, and immediate fields need to be extracted
            reg_mask = (0b1111 << 8)
            reg1 = (instruction & reg_mask) >> 8
            imm_mask = 0b11111111
            imm = instruction & imm_mask
            reg2 = None
            tgt = None
            return op, reg1, reg2, imm, tgt

        else:
            # For R-Format instructions the op code, register 1, and register 2 fields are extracted
            reg1_mask = (0b1111 << 8)
            reg2_mask = (0b1111 << 4)
            reg1 = (instruction & reg1_mask) >> 8
            reg2 = (instruction & reg2_mask) >> 4
            imm = None
            tgt = None
            return op, reg1, reg2, imm, tgt

    def execute(self, op, reg1, reg2, imm, tgt):
        # This function calls the function corresponding to the instruction
        # and passes in the values for the relevant fields
        if op == 0:
            self.add(reg1, reg2)
        if op == 1:
            self.sub(reg1, reg2)
        if op == 2:
            self.rand(reg1, imm)
        if op == 3:
            self.load(reg1, reg2)
        if op == 4:
            self.store(reg2, reg1)
        if op == 5:
            self.jal(tgt)
        if op == 6:
            self.jr(reg1)
        if op == 7:
            self.beq(reg1, imm)
        if op == 8:
            self.bgt(reg1, imm)
        if op == 9:
            self.set(reg1, reg2)
        if op == 10:
            self.seti(reg1, imm)

    def setreg(self, reg, data):
        # don't allow writes into registers $0 ($zero) and $1 ($one)
        if reg == 0 or reg == 1:
            return

        # constrain data to 16 bits (a bit hacky to do it here, but oh well)
        data = data & 0xffff

        self.regfile[reg] = data

    def add(self, reg1, reg2):
        # reg1 = reg1 + reg2
        result = self.regfile[reg1] + self.regfile[reg2]
        self.setreg(reg1, result)

    def sub(self, reg1, reg2):
        # reg1 = reg1 - reg 2
        result = self.regfile[reg1] - self.regfile[reg2]
        self.setreg(reg1, result)

    def seti(self, reg1, imm):
        # reg1 = immediate
        # If the most significant bit of the immediate is a 1
        # then the immediate is negative and must be adjusted accordingly
        if imm > 0b1111111:
            imm -= 256
        self.setreg(reg1, imm)

    def set(self, reg1, reg2):
        # reg1 = reg2
        self.setreg(reg1, self.regfile[reg2])

    def jr(self, reg1):
        # PC = address in reg1
        self.PC = self.regfile[reg1]

    def jal(self, tgt):
        # Current PC is stored in $15
        # PC = Immediate (target)
        self.regfile[15] = self.PC
        self.PC = tgt

    def load(self, reg1, reg2):
        addr = self.regfile[reg2]
        # If the address is <256, it is I/O
        # If the address is <256, it is I/O
        if addr < 0x100:
            # Only current input device: buttons
            if addr < _NUMBUTTONS:
                data = self.buttons[addr]
            else:
                raise Exception(
                        f"Invalid input address: {addr}  (valid input addresses: 0-{_NUMBUTTONS-1})"
                )
        else:
            # data = Value in Data Memory at address reg2
            data = self.dmem[self.regfile[reg2]]
        # reg1 gets data read from I/O or DMEM
        self.setreg(reg1, data)

    def store(self, reg2, reg1):
        addr = self.regfile[reg2]
        data = self.regfile[reg1]
        # If the address is <256, it is I/O
        if addr < 0x100:
            # Only current output device: LED matrix
            if addr < _MATRIXSIZE**2:
                # we need to update the LED display
                self.matrix[addr // 10][addr % 10] = data
        else:
            # Data Memory at address reg2 = Value of reg1
            self.dmem[addr] = data

    def beq(self, reg1, imm):
        # if reg1 == implicit register, jump to PC + immediate
        if self.regfile[reg1] == self.regfile[15]:
            # If the most significant bit of the immediate is a 1
            # then the immediate is negative and must be adjusted accordingly
            if imm > 0b1111111:
                imm -= 256
            self.PC += imm
            # Subtract 1 from PC to counteract our addition in the step function
            self.PC -= 1
        else:
            pass

    def bgt(self, reg1, imm):
        # if reg1 > implicit register, jump to PC + immediate
        if self.regfile[reg1] > self.regfile[15]:
            # If the most significant bit of the immediate is a 1
            # then the immediate is negative and must be adjusted accordingly
            if imm > 0b1111111:
                imm -= 256
            self.PC += imm
            # Subtract 1 from PC to counteract our addition in the step function
            self.PC -= 1
        else:
            pass

    def rand(self, reg1, imm):
        # reg1 = random value from 0-immediate
        self.setreg(reg1, random.randint(0, imm))
