#
# S20_SIM.py  --  Simulator class for the SIM CPU designed by CS256-S20.
#

from utils import print_val, print_mem, print_input, print_matrix


# Constants for this architecture
_NUMREG = 8       # number of registers in the register file
_REGSIZE = 8      # size (in bits) of each register)
_ADDRSIZE = _REGSIZE  # size (in bits) of DMEM addresses
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
        with open(filename, 'r') as f:
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
            raise Exception(f"Incorrect number of buttons.  Got {len(buttons)}, expected {_NUMBUTTONS}.")
        if max(buttons) > 1 or min(self.buttons) < 0:
            raise Exception(f"Invalid value for button.  Only allowed values are 0 and 1.")
        self.buttons = buttons

    def step_n(self, n):
        # Simulate n cycles of the CPU (see self.step()).
        for _ in range(n):
            self.step()

    def step(self):
        # Simulate *one* cycle of the CPU (Fetch-Decode-Execute)
        # Basic outline:
        #  1) Fetch the current instruction (using imem and PC)
        #  2) Decode the instruction into its different fields
        #  3) Execute the instruction by updating the CPU state
        #     according to what the execution of that instruction
        #     would do.
        pass

    def reset(self):
        # Reset the CPU state to just-powered-on, with everything but IMEM cleared
        self.PC = 0
        self.regfile = [0] * _NUMREG
        self.dmem = [0] * 2**_ADDRSIZE
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
