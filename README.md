# 256sim

256sim is a CPU simulator for the student-designed ISAs from CS 256 (Computer
Organization and Architecture) at Illinois Wesleyan University.  Each year,
students design a new ISA from scratch (though heavily influenced by MIPS,
which they learn earlier in the semester), design a datapath for it, and
implement their CPU in [Logisim](http://www.cburch.com/logisim/), in a
simulator (this program) and on physical breadboards.

The simulator can be run via the command line as ``256sim.py``.

![256sim screenshot](docs/256sim_screenshot.png?raw=true)

Asciinema demo:

[![demo](https://asciinema.org/a/9qoZyN8gmCZDfo0buELqGj2bD.svg)](https://asciinema.org/a/9qoZyN8gmCZDfo0buELqGj2bD?autoplay=1)

## Usage

Run `256sim.py` on the command line to launch the simulator.  Specify an
architecture, and optionally specify a machine code file to load from the
command line like:
```bash
$ python3 ./256sim.py ARCH
# or
$ python3 ./256sim.py ARCH FILE.bin
```

The architecture (ARCH) should be the name of an architecture simulator module
placed under `archs/`.  Specify the name of the Python file without the `.py`
suffix.  If you run `python3 ./256sim.py` without any arguments, it will show
you the possible architecture names it finds in `arch/` itself.

At the simulator's prompt, press <kbd>ENTER</kbd> with no command to step
forward one cycle in the simulation.

<kbd>S 200</kbd> will step forward 200 cycles, updating the display when
finished.

<kbd>W 2000</kbd> will watch 2000 cycles of execution, updating the display as
the simulation runs.

See the built-in help (<kbd>H</kbd>) for more commands and options.

### Windows

The UI uses [ANSI codes](https://en.wikipedia.org/wiki/ANSI_escape_code) to
color parts of the interface.  Windows terminals might not support these by
default.  If you're running this under Windows, install and use [Windows
Terminal](https://github.com/microsoft/terminal) to get proper support for ANSI
colors and other benefits.


## Architectures

A simulator for a given architecture can be made by copying
`simulator_template.py` to `[architecture name].py` and implementing the
`step()` method.

Then, place the new file in `archs` and run the simulator with
that architecture by specifying the architecture name (*without*
`.py`) as a command line argument.

## Dependencies

The code is compatible with Python 3.10+ with no dependencies beyond the
Python standard library.

## Authors

Developed by Mark Liffiton.

ISA simulation code contributed by Jonathan Nocek, Kyle Wheat, and Ray Loerke.

