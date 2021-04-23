import math
import shutil


def print_head(string):
    print(f"[1;4;33m{string}[m")


def print_val(val, name):
    print_head(name)
    print(val)


# store previous version of each array to highlight changes
_mem_cache = {}


def print_mem(array, name, val_width=8, min_addr=0, label_all=False, highlight=None, limit_to_modified=False, limit_to_nonzero=False):
    addrsize = math.ceil(math.log2(len(array))/4)
    valsize = math.ceil(val_width/4)

    t_columns, t_rows = shutil.get_terminal_size(fallback=(80, 24))
    row_len = 1 if (label_all) else (t_columns - addrsize - 1) // (valsize + 1)

    print_head(name)

    try:
        prev, max_mod_addr = _mem_cache[name]
        assert len(prev) == len(array)  # so we ignore it if it's a different length
    except (KeyError, AssertionError):
        prev = array
        max_mod_addr = -1

    def row_to_str(row_both, offset):
        # Turn a row of a memory into a printable string
        # row_both contains current and previous values, zipped
        # offset is the address of the first element in the given row
        return f"{offset:0{addrsize}x}: " + ' '.join(
            (
                ("[34;1;4m" if x != prev_x or i+offset == highlight else "")
                +
                f"{x:0{valsize}x}"
                +
                ("[m" if x != prev_x or i+offset == highlight else "")
            ) for i, (x, prev_x) in enumerate(row_both)
        )

    # For matched current/prev values to calc max_mod_addr and for row_to_str()
    both = list(zip(array, prev))

    # Find the maximum index that differs in the array from last time, if anything changed
    if array != prev:
        max_mod_addr_now = max(i for i, pair in enumerate(both) if pair[0] != pair[1])
        # Take the highest of either that index or our previous max
        max_mod_addr = max(max_mod_addr, max_mod_addr_now)

    # Calculate the maximum address to print based on specified arguments
    max_addr = len(array) - 1
    if limit_to_nonzero:  # only works if there is at least one non-zero element...
        max_addr = max(i for i, val in enumerate(array) if val != 0)
    if limit_to_modified:
        max_addr = min(max_addr, max_mod_addr)

    mem_str = '\n'.join(
        row_to_str(both[i : i+row_len], i)
        for i in range(min_addr, max_addr+1, row_len)
    )
    print(mem_str)
    if limit_to_modified and max_addr != len(array):
        print(f"[34m[Remaining addresses not modified since start of simulation.][m")

    # Store the current contents and our maximum modified address for next time
    _mem_cache[name] = array[:], max_mod_addr


def print_input(buttons, name):
    print_head(name)

    num = len(buttons)

    print("┌─" + "┬─"*(num-1) + "┐")
    print("│" + "│".join(str(i) for i in buttons) + "│")
    print("└─" + "┴─"*(num-1) + "┘")


def print_matrix(matrix, name):
    print_head(name)

    matrix_str = '\n'.join(
        ''.join(
            '[31m█[m' if matrix[row][col] else '[30m█[m'
            for col in range(len(matrix[row]))
        )
        for row in range(len(matrix))
    )
    print(matrix_str)
