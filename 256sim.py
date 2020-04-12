#!/bin/env python3

from S20_SIM import Simulator


def read_cmd():
    # Show a prompt and read a command from the terminal
    cmd = input("[1;32mCommand[0;32m (L)oad machine code | Change (B)utton state | (S)tep | (R)eset | (Q)uit[1;32m:[m ")
    cmd = cmd.upper()
    return cmd


def main():
    # Instantiate the Simulator object
    sim = Simulator()

    # REPL:
    #  Read a command
    #  Evaluate that command (potentially running
    #    one or more steps of simulation)
    #  Print the current state of the simulation
    #  Loop
    while True:
        print()
        cmd = read_cmd()

        if cmd == 'L':
            filename = input("[1;32mBinary file:[m ")
            try:
                sim.load_bin(filename)
            except Exception as e:
                print(f"[1;31mError loading file:[m {e}")
                continue
        elif cmd == 'B':
            buttons = input("[1;32mNew state[0;32m (4 buttons; 0 or 1 each; e.g. '0010' to press just the third button)[1;32m:[m ")
            try:
                sim.change_buttons(buttons)
            except Exception as e:
                print(f"[1;31mInvalid button string:[m {e}")
                continue
        elif cmd == 'S':
            sim.step()
        elif cmd == 'R':
            sim.reset()
        elif cmd == 'Q':
            break

        sim.print()


if __name__ == "__main__":
    main()
