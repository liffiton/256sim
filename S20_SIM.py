#
# S20_SIM.py  --  Simulator class for the SIM CPU designed by CS256-S20.
#
# Authors: Mark Liffiton, Jonathan Nocek, Kyle Wheat
#
from utils import print_val, print_mem, print_input, print_matrix

import random
import time

# Constants for this architecture
_NUMREG = 8  # number of registers in the register file
_REGSIZE = 8  # size (in bits) of each register)
_ADDRSIZE = _REGSIZE  # size (in bits) of DMEM addresses
_NUMBUTTONS = 4  # Number of buttons (binary on/off) for input
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
        buttons = [int(c) for c in new_buttons]
        if len(buttons) != _NUMBUTTONS:
            raise Exception(
                f"Incorrect number of buttons.  Got {len(buttons)}, expected {_NUMBUTTONS}."
            )
        if max(buttons) > 1 or min(self.buttons) < 0:
            raise Exception(
                f"Invalid value for button.  Only allowed values are 0 and 1."
            )
        self.buttons = buttons

    def step_n(self, n):
        # Simulate n cycles of the CPU (see self.step()).
        for _ in range(n):
            self.step()

    def watch_n(self, n):
        # Simulate n cycles of the CPU, as in step_n(), but watch the
        # state of the CPU by printing after every 10th cycle.
        for i in range(n):
            self.step()
            if i % 10 == 0:
                print("[2J[H")  # clear the screen and return to home position
                self.print()
                time.sleep(0.05)

    def step(self):
        # Simulate *one* cycle of the CPU (Fetch-Decode-Execute)
        # Basic outline:
        #  1) Fetch the current instruction (using imem and PC)
        #  2) Decode the instruction into its different fields
        #  3) Execute the instruction by updating the CPU state
        #     according to what the execution of that instruction
        #     would do.
        word = self.fetch()
        op, r1, r2, imm, func = self.decode(word)
        self.execute(op, r1, r2, imm, func)

    def reset(self):
        # Reset the CPU state to just-powered-on, with everything but IMEM cleared
        self.PC = 0
        self.regfile = [0] * _NUMREG
        self.dmem = [0] * 2 ** _ADDRSIZE
        self.buttons = [0] * _NUMBUTTONS
        self.matrix = [([0] * _MATRIXSIZE) for _ in range(_MATRIXSIZE)]

    def print(self):
        # Print the current state of all state (memory) elements of the CPU
        print_val(self.PC, "PC")
        print_mem(self.imem, "IMEM", val_width=16)
        print_mem(self.regfile, "Regfile", label_all=True)
        print_mem(self.dmem, "DMEM")
        print_input(self.buttons, "Input")
        print_matrix(self.matrix, "Output")

    def fetch(self):
        """Fetch word in imem using the program counter, then increment PC

        Returns:
            word -- Fetched word from imem
        """
        word = self.imem[self.PC]
        self.PC += 1
        return word

    def decode(self, word):
        """Decode word and parse to components of R-type and I-Type instuctions

        Arguments:
            word -- Gathered via fetch()

        Returns:
            opcode -- Both I-Type and R-Type
            r1 -- Both I-Type and R-Type
            r2 -- Only for R-Type, None for I-Type
            imm -- Only for I-Type, None for R-Type
            func -- Only for R-Type, None for I-Type
        """
        opcode_mask = 0b111 << 13
        opcode = (word & opcode_mask) >> 13
        # If opcode is 0, parse word for R-type instruction
        if opcode == 0:
            r1_mask = 0b111 << 10
            r1 = (word & r1_mask) >> 10

            r2_mask = 0b111 << 7
            r2 = (word & r2_mask) >> 7

            func_mask = 0b1111111
            func = word & func_mask
            imm = None
            return opcode, r1, r2, imm, func

        # If opcode is not 0, parse word for I-type instruction
        else:
            r1_mask = 0b111 << 10
            r1 = (word & r1_mask) >> 10

            immediate_mask = 0b1111111111
            imm = word & immediate_mask
            r2 = None
            func = None
            return opcode, r1, r2, imm, func

    def execute(self, op, r1, r2, imm, func):
        """Execute instruction

        Arguments:
            op -- Opcode Code
            r1 -- Register 1
            r2 -- Register 2
            imm -- Immediate Value
            func -- Function code
        """
        if op == 0:
            if func == 0:
                self._add(r1, r2)
            if func == 1:
                self._sub(r1, r2)
            if func == 2:
                self._load(r1, r2)
            if func == 3:
                self._store(r1, r2)
            if func == 4:
                self._in(r1, r2)
            if func == 5:
                self._out(r1, r2)
            if func == 6:
                self._sgt(r1, r2)

        else:
            if op == 1:
                self._addi(r1, imm)
            if op == 2:
                self._assigni(r1, imm)
            if op == 3:
                self._beq(r1, imm)
            if op == 4:
                self._bne(r1, imm)
            if op == 5:
                self._rand(r1, imm)

    def _add(self, r1, r2):
        """
        r1 = r1 + r2
        R-format
        """
        self.regfile[r1] += self.regfile[r2]

    def _addi(self, r1, imm):
        """
        r1 = r1 + imm
        I-format
        """
        # correct for negative immediates (not parsed as negative so far)
        if imm > 0b111111111:
            imm -= 1024
        self.regfile[r1] += imm

    def _assigni(self, r1, imm):
        """
        r1 = imm
        I-format
        """
        # correct for negative immediates (not parsed as negative so far)
        if imm > 0b111111111:
            imm -= 1024
        self.regfile[r1] = imm

    def _sub(self, r1, r2):
        """
        r1 = r1 - r2
        R-format
        """
        self.regfile[r1] -= self.regfile[r2]

    def _load(self, r1, r2):
        """
        r1 = Mem[r2]
        R-format
        """
        self.regfile[r1] = self.dmem[r2]

    def _store(self, r1, r2):
        """
        Mem[r2] = r1
        R-format
        """
        self.dmem[r2] = self.regfile[r1]

    def _beq(self, r1, label):
        """
        If (r1 == $7) goto label [implicitly, $7 is always used in the comparison]
        I-format
        """
        if self.regfile[r1] == self.regfile[7]:
            # correct for negative immediates (not parsed as negative so far)
            if label > 0b111111111:
                label -= 1024
            self.PC += label
            # correct for automatic PC += 1
            self.PC -= 1
        else:
            pass

    def _bne(self, r1, label):
        """
        If (r1 != $7) goto label [implicitly, $7 is always used in the comparison]
        I-format
        """
        if self.regfile[r1] != self.regfile[7]:
            # correct for negative immediates (not parsed as negative so far)
            if label > 0b111111111:
                label -= 1024
            self.PC += label
            # correct for automatic PC += 1
            self.PC -= 1
        else:
            pass

    def _sgt(self, r1, r2):
        """
        $7 = (r1 > r2) ? 1 : 0 [implicitly, $7 is always used in the comparison]
        R-format
        """
        if self.regfile[r1] > self.regfile[r2]:
            self.regfile[7] = 1
        else:
            self.regfile[7] = 0

    def _in(self, r1, r2):
        """
        r1 = IO[r2]
        R-format
        """
        self.regfile[r1] = self.buttons[r2]

    def _out(self, r1, r2):
        """
        IO[r2] = r1
        R-format
        """
        x = self.regfile[r2] % _MATRIXSIZE
        y = self.regfile[r2] // _MATRIXSIZE
        self.matrix[y][x] = self.regfile[r1]

    def _rand(self, r1, imm):
        """
        r1 = [randvalue] & imm    [randvalue is a random 8-bit value]
        I-format
        """
        randvalue = random.getrandbits(8)
        self.regfile[r1] = randvalue & imm
