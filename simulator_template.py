#
# simulator_template.py  --  Simulator class template for 256sim.
#
# Authors: Mark Liffiton
#
from print_utils import print_val, print_mem, print_input, print_matrix

import time

# Constants for this architecture
_NUMREG = 1       # number of registers in the register file
_REGSIZE = 1      # size (in bits) of each register)
_ADDRSIZE = 1     # size (in bits) of DMEM addresses
_NUMBUTTONS = 1   # Number of buttons (binary on/off) for input
_MATRIXSIZE = 1   # width and height of the pixel matrix output


class Simulator:
    def __init__(self) -> None:
        # CPU state:
        self.imem : list[int] = [0]  # not affected by CPU reset, so only initialized here
        # Simulator state (separate from the CPU itself):
        self.bin_filename : str = ""

        # Initialize most state using .reset()
        self.reset()

    def load_bin(self, filename : str) -> None:
        """ Load machine code from a file into instruction memory.

        Parameters:
         - filename: String of a path to a file containing machine code for
                     instruction memory.  Machine code words should be written
                     in hexadecimal, separated by whitespace.
        """
        self.bin_filename = filename
        with open(filename, "r") as f:
            data = f.read()
        words = data.split()
        self.imem = [int(word, 16) for word in words]

        # Always reset on loading new code
        self.reset()

    def reset(self) -> None:
        """ Reset the CPU state to just-powered-on, with everything but IMEM cleared. """
        self.PC: int = 0
        self.regfile: list[int] = [0] * _NUMREG
        self.dmem: list[int] = [0] * 2 ** _ADDRSIZE
        self.buttons: list[int] = [0] * _NUMBUTTONS
        self.matrix: list[list[int]] = [([0] * _MATRIXSIZE) for _ in range(_MATRIXSIZE)]

    def change_buttons(self, new_buttons : str) -> None:
        """ Change the state of the simulated buttons.

        Parameters:
         - new_buttons: String containing a 0 or 1 for each button
                        e.g. "0110" for the first button not pressed, the
                        second and third pressed, and the fourth not pressed.
        """
        buttonvals = [int(c) for c in new_buttons]
        if len(buttonvals) != _NUMBUTTONS:
            raise Exception(
                f"Incorrect number of buttons.  Got {len(buttonvals)}, expected {_NUMBUTTONS}."
            )
        if max(buttonvals) > 1 or min(buttonvals) < 0:
            raise Exception("Invalid value for button.  Only allowed values are 0 and 1.")
        self.buttons = buttonvals

    def step_n(self, n: int) -> None:
        """ Simulate n cycles of the CPU (see self.step()). """
        for _ in range(n):
            self.step()

    def watch_n(self, n: int) -> None:
        """ Simulate n cycles of the CPU, as in step_n(), but watch the
            state of the CPU by printing after every 100th cycle.
        """
        for i in range(n):
            self.step()
            if i % 100 == 0:
                print("[2J[H")  # clear the screen and return to home position
                self.print()
                time.sleep(0.05)    # simulate ~2kHz clock rate

    def run_until(self, pc_breakpoint: int) -> None:
        """ Simulate until the given breakpoint is reached.

        Parameters:
         - pc_breakpoint: int of the address at which execuation should stop
        """
        # always execute at least once -- allows repeatedly running to the same instruction
        self.step()
        while self.PC != pc_breakpoint:
            self.step()

    def print(self) -> None:
        """ Print the current state of all state (memory) elements of the CPU. """
        print_val(self.PC, "PC")
        print_mem(self.imem, "IMEM", val_width=16, highlight=self.PC)
        print_mem(self.regfile, "Regfile", label_all=True)
        print_mem(self.dmem, "DMEM", limit_to_modified=True)
        print_input(self.buttons, "Input")
        print_matrix(self.matrix, "Output")

    def step(self) -> None:
        """ Simulate *one* cycle of the CPU (Fetch-Decode-Execute)
        Basic outline:
          1) Fetch the current instruction (using imem and PC)
          2) Decode the instruction into its different fields
          3) Execute the instruction by updating the CPU state
             according to what the execution of that instruction
             should do according to the ISA specification.
        """
        pass

###
# Tips and Recommendations
###
#
# 1) Create separate methods for fetch, decode, and execute.  Then create separate
#    methods for every different instruction.  Pass the arguments for each instruction
#    into its corresponding method when it is executed.
#
# 2) You can write binary literals in Python with the 0b prefix.  E.g.,  0b01101100
#    Hexadecimal can be written with the 0x prefix.  E.g.,  0x6c
#
# 3) Use bitwise logical operators to mask and extract bits from a single instruction.
#    This can be used to pull separate fields out of a single binary instruction.
#
# 4) Make sure you're clear on what the following are and what they hold / how they work:
#
#      self.PC, self.imem, self.regfile, self.dmem, self.buttons, self.matrix
#
#    Mostly they're arrays.  Look at the reset() method to see how they're initialized.
#    The result of executing any instruction should be that some of these are modified.
#    Ask me for clarification if you're unsure about any of them.
#
# 5) Take it one small step at a time, and test everything you implement before moving on!
#
