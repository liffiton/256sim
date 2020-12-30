import math
import shutil


def print_head(string):
    print(f"[1;4;33m{string}[m")


def print_val(val, name):
    print_head(name)
    print(val)


# store previous version of each array to highlight changes
_mem_cache = {}


def print_mem(array, name, val_width=8, label_all=False, highlight=None):
    addrsize = math.ceil(math.log2(len(array))/4)
    valsize = math.ceil(val_width/4)

    t_columns, t_rows = shutil.get_terminal_size(fallback=(80, 24))
    row_len = 1 if (label_all) else (t_columns - 4) // (valsize + 1)

    print_head(name)

    try:
        prev = _mem_cache[name]
        assert len(prev) == len(array)  # so we ignore it if it's a different length
    except (KeyError, AssertionError):
        prev = array

    both = list(zip(array, prev))

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

    mem_str = '\n'.join(
        row_to_str(both[i : i+row_len], i)
        for i in range(0, len(array), row_len)
    )
    print(mem_str)

    _mem_cache[name] = array[:]  # make a copy


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
