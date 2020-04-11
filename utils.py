import math
import shutil


def print_head(string):
    print(f"[1;4;33m{string}[m")


def print_val(val, name):
    print_head(name)
    print(val)


def print_mem(array, name, val_width=8, label_all=False):
    addrsize = math.ceil(math.log2(len(array))/4)
    valsize = math.ceil(val_width/4)

    t_columns, t_rows = shutil.get_terminal_size(fallback=(80, 24))
    row_len = 1 if (label_all) else (t_columns - 4) // (valsize + 1)

    print_head(name)

    imem_str = '\n'.join(
        f"{i:0{addrsize}x}: " + ' '.join(
            f"{x:0{val_width//4}x}" for x in array[i:i+row_len]
        )
        for i in range(0, len(array), row_len)
    )
    print(imem_str)


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
