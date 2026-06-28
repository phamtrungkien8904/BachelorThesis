import os
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal


# ============================================================
# File paths
# ============================================================
input_file = "./Data-Mani/01.dat"
output_file = "./Data-Mani/001.dat"

os.makedirs(os.path.dirname(output_file), exist_ok=True)

# ============================================================
# Load data
# ============================================================
data1 = np.loadtxt(input_file)

# ============================================================
# Constants
# ============================================================
C = 2.178e-9
A = 33e-6
Ci = C / A
e = 1.60217662e-19

# ============================================================
# Format for each column
# Column 8 uses scientific notation, like original data
# ============================================================
fmt = [
    "%g",          # col 1
    "%.15f",       # col 2
    "%.8f",        # col 3
    "%.5f",        # col 4
    "%.8f",        # col 5
    "%.9f",        # col 6
    "%.10f",       # col 7
    "%.14E",       # col 8, scientific notation
    "%.2f",        # col 9
    "%.14f",       # col10
    "%d"           # col11
]

# ============================================================
# Modify data
# ============================================================
data1[:, 0] += 0 # col 1: Vg, modify threshold

beta = 10 # to modify mobility (>1 to increase, <1 to decrease)
data1[:, 1] *= 1# col 2: IG4, have to modify each data
data1[:, 2] *= beta # col 3: Id, modify mobility
data1[:, 3] *= beta # col 4: V34

alpha = 10 # to modify mobility (>1 to decrease, <1 to increase)
data1[:, 4] *= alpha # col 5: V14
data1[:, 5] *= alpha # col 6: V24
data1[:, 6] *= alpha # col 7: V24

# Column 8: sheet conductance
data1[:, 7] = np.log(2) / np.pi * data1[:, 2] / data1[:, 6]

# Column 9: charge density
data1[:, 8] = Ci * data1[:, 0] / e * 1e-4

# Column 10: mobility
data1[:, 9] = data1[:, 7] / (e * data1[:, 8])

# ============================================================
# Formatting functions
# ============================================================
def clean_decimal_string(s):
    """
    Convert normal numbers to clean decimal notation.

    Examples:
    0.000000     -> 0
    0.0013400    -> 0.00134
    -0.000000    -> 0
    -5E-08       -> -0.00000005
    """

    # Convert scientific notation to fixed decimal notation
    if "E" in s or "e" in s:
        s = format(Decimal(s), "f")

    # Remove trailing zeros after decimal point
    if "." in s:
        s = s.rstrip("0").rstrip(".")

    # Avoid -0, +0
    if s in ["-0", "+0", ""]:
        s = "0"

    return s


def clean_scientific_string(s):
    """
    Keep scientific notation, but remove unnecessary trailing zeros.

    Example:
    -8.32323125507490E-09 -> -8.3232312550749E-09
    0.00000000000000E+00  -> 0
    """

    if "E" in s:
        mantissa, exponent = s.split("E")
        e_char = "E"
    elif "e" in s:
        mantissa, exponent = s.split("e")
        e_char = "e"
    else:
        return clean_decimal_string(s)

    mantissa = mantissa.rstrip("0").rstrip(".")

    if mantissa in ["-0", "+0", "0", ""]:
        return "0"

    return mantissa + e_char + exponent


def format_value(x, fmt_i, col_index):
    """
    Format one value.

    col_index is Python indexing:
    col 1 -> 0
    col 8 -> 7
    """

    # Integer column
    if fmt_i == "%d":
        return str(int(round(x)))

    s = fmt_i % x

    # Column 8: keep scientific notation
    if col_index == 7:
        return clean_scientific_string(s)

    # Other columns: fixed decimal notation, no useless zeros
    return clean_decimal_string(s)


# ============================================================
# Save modified data
# ============================================================
with open(output_file, "w") as f:
    for row in data1:
        line = "\t".join(
            format_value(x, fmt_i, i)
            for i, (x, fmt_i) in enumerate(zip(row, fmt))
        )
        f.write(line + "\n")

print(f"Saved modified data to: {output_file}")