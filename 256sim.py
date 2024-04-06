#!/bin/env python3
#
# 256sim.py -- Command-line simulation of the CS256-S20 SIM CPU.
#
# Author: Mark Liffiton
# Date: April, 2020
#

import argparse
import importlib
import pathlib
import readline  # noqa--  Automatically adds command history (via up/down keys)


def read_cmd():
    # Show a prompt and read a command from the terminal
    cmd = input("[1;32mCommand[0;32m (H)elp | (L)oad | (B)utton | (S)tep | (W)atch | Run (U)ntil | (R)eset | (Q)uit[1;32m:[m ")
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
    (W)atch  -- Watch the simulation over multiple clock cycles.  Specify a number
                of cycles to simulate after the command (e.g., "w 10000").  The
                state of the CPU is continuously displayed as the simulation runs.
    Run (U)ntil
             -- Run the simulation until the PC reaches the specified value.
                Useful when debugging!  Run until a given instruction is reached.
    (R)eset  -- Reset the state of the CPU, clearing all memory elements except
                the instruction memory.
    (Q)uit   -- Exit the simulation.

    Commands are case insensitive.""")


def main():
    parser = argparse.ArgumentParser(description="Simulate a CS256-designed CPU.")
    # Find all files archs/*.py, strip the .py part
    archs = [p.name[:-3] for p in pathlib.Path(".").glob("archs/*.py")]
    parser.add_argument("architecture", choices=archs)
    parser.add_argument("binfile", nargs="?")
    args = parser.parse_args()

    arch = importlib.import_module(f"archs.{args.architecture}")

    # Instantiate the Simulator object
    sim = arch.Simulator()

    # Allow a bin file to be specified on the command line
    if args.binfile:
        try:
            sim.load_bin(args.binfile)
        except Exception as e:
            print(f"[1;31mError loading file:[m {e}")
            return

        # Print state once to start if code already loaded
        sim.print()

    # REPL:
    #  Read a command
    #  Evaluate that command (potentially running
    #    one or more steps of simulation)
    #  Print the current state of the simulation
    #  Loop
    while True:
        cmd, args = read_cmd()

        # help doesn't print the state again, just goes straight to another prompt
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
            num_buttons = arch._NUMBUTTONS  # ideally would be a method of the Simulator class...
            example = f"{1:0{num_buttons}x}"
            buttons = args[0] if args else input(f"[1;32mNew state[0;32m ({num_buttons} buttons; 0 or 1 each; e.g. '{example}' to press just the last button)[1;32m:[m ")
            try:
                sim.change_buttons(buttons)
            except Exception as e:
                print(f"[1;31mInvalid button string:[m {e}")
                continue

        elif cmd[0] == 'S':
            n = int(args[0]) if args else 1
            sim.step_n(n)

        elif cmd[0] == 'W':
            if not args:
                print("[1;31mWatch command requires a number of cycles to watch.  (E.g., 'W 10000'[m")
                continue
            n = int(args[0])
            sim.watch_n(n)

        elif cmd[0] == 'U':
            if not args:
                print("[1;31mRun Until command requires a target PC value.  (E.g., 'U 12'[m")
                continue
            tgt = int(args[0])
            sim.run_until(tgt)

        elif cmd[0] == 'R':
            sim.reset()

        elif cmd[0] == 'Q':
            break

        sim.print()


if __name__ == "__main__":
    main()
