#!/bin/env python3

from S20_SIM import Simulator


def read_cmd():
    # Show a prompt and read a command from the terminal
    cmd = input("[1;32mCommand[0;32m (H)elp | (L)oad machine code | Change (B)utton state | (S)tep | (R)eset | (Q)uit[1;32m:[m ")
    if cmd:
        parts = cmd.strip().split()
        return parts[0].upper(), parts[1:]
    else:
        return "S", []


def print_help():
    print("""
Commands:
    (H)elp   -- Print this help message.
    (L)oad machine code
             -- Load machine code from a file into instruction memory.
                Optionally write the filename after the command (e.g., "l
                test.bin").  If a filename is not given, you will be prompted
                to enter one separately.
    Change (B)utton state
             -- Change the state (pressed or not pressed) of the simulated
                buttons.  Each button is set to 1 (pressed) or 0 (not pressed).
                Optionally write the buttons state after the command (e.g., "b
                0101").  If only the command is given, you will be prompted to
                enter the state separately.
    (S)tep   -- Step the simulation forward one clock cycle / one instruction.
                Optionally specify a number of cycles to simulate after the
                command (e.g., "s 10").
                (Pressing enter with no command entered will also execute Step.)
    (R)eset  -- Reset the state of the CPU, clearing all memory elements except
                the instruction memory.
    (Q)uit   -- Exit the simulation.

    Commands are case insensitive.""")


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
        cmd, args = read_cmd()

        if cmd[0] == 'H':
            print_help()
            continue

        elif cmd[0] == 'L':
            filename = args[0] if args else input("[1;32mBinary file:[m ")
            try:
                sim.load_bin(filename)
            except Exception as e:
                print(f"[1;31mError loading file:[m {e}")
                continue

        elif cmd[0] == 'B':
            buttons = args[0] if args else input("[1;32mNew state[0;32m (4 buttons; 0 or 1 each; e.g. '0010' to press just the third button)[1;32m:[m ")
            try:
                sim.change_buttons(buttons)
            except Exception as e:
                print(f"[1;31mInvalid button string:[m {e}")
                continue

        elif cmd[0] == 'S':
            n = int(args[0]) if args else 1
            sim.step_n(n)

        elif cmd[0] == 'R':
            sim.reset()

        elif cmd[0] == 'Q':
            break

        sim.print()


if __name__ == "__main__":
    main()
