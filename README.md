# 256sim

256sim is a CPU simulator for the student-designed ISAs from CS 256 (Computer
Organization and Architecture) at Illinois Wesleyan University.  Each year,
students design a new ISA from scratch (though heavily influenced by MIPS,
which they learn earlier in the semester), design a datapath for it, and
implement their CPU in [Logisim](http://www.cburch.com/logisim/), in a
simulator (this program) and on physical breadboards.

The simulator can be run via the command-line as ``256sim.py``.

![256sim screenshot](docs/256sim_screenshot.png?raw=true)

Asciinema demo:

[![demo](https://asciinema.org/a/WMgPVtNbGgCrk4hIxw5eZFirF.svg)](https://asciinema.org/a/WMgPVtNbGgCrk4hIxw5eZFirF?autoplay=1)

## Usage

Run `256sim.py` to launch the simulator.  You can optionally specify a machine
code file to load from the commandline like:
```bash
$ ./256sim.py FILE.bin
```

At the simulator's prompt, press <kbd>ENTER</kbd> with no command to step
forward one cycle in the simulation.

<kbd>S 200</kbd> will step forward 200 cycles, updating the display when
finished.

<kbd>W 2000</kbd> will watch 2000 cycles of execution, updating the display as
the simulation runs.

See the built-in help (<kbd>H</kbd>) for more commands and options.

## Dependencies

The code is compatible with Python 3.6+ with no dependencies beyond the
Python standard library.

## Authors

Developed by Mark Liffiton.

S20-SIM ISA simulation code contributed by Jonathan Nocek and Kyle Wheat.
