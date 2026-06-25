
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys

File_index = sys.argv[1] # Get the file index from command line argument

# Custom settings for python figures
plt.style.use('classic')

# plt.rcParams.update({
#     "text.usetex": True,
#     'text.latex.preamble': r'''
#     \usepackage[T1]{fontenc}
#     \usepackage{lmodern}
#     \usepackage[utf8]{inputenc}
#     \usepackage{amsmath}
#     \usepackage{amssymb}
#     \usepackage{siunitx}
#     \usepackage{sfmath}
#     '''
# })
plt.rcParams.update({
    # Figure settings
    'figure.dpi': 300,
    'figure.figsize': (10/2.54, 8/2.54),  # 10x6 cm in inches (1 figure per line)
    # 'figure.figsize': (8/2.54, 6/2.54),  # 10x6 cm in inches (2 figures per line)
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.linewidth': 1,
    'axes.labelsize': 8,
    'axes.titlesize': 8,
    'axes.labelcolor': 'black',
    'savefig.facecolor': 'white',
    'font.family': 'sans-serif',
    'font.sans-serif': 'Arial',
    # 'mathtext.fontset': 'cm',
    'figure.constrained_layout.use': True,

    # Ticks
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 4,
    "ytick.major.size": 4,
    "xtick.major.width": 1,
    "ytick.major.width": 1,
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "xtick.minor.size": 0,
    "ytick.minor.size": 0,
    "xtick.minor.width":0,
    "ytick.minor.width": 0,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,  

    # Legend
    'legend.frameon': False,
    'legend.title_fontsize': 8,
    'legend.fontsize': 8,
    'legend.handlelength': 2,
    'legend.loc': 'best',
    'legend.numpoints': 1,

    # Line style
    'lines.linestyle': '-',
    'lines.linewidth': 1,
    'lines.markersize': 4,
    'lines.markeredgecolor': 'white',
    'lines.markeredgewidth': 0.5,
})

markevery = 10

C = 1.8e-9
A = 32e-6
Ci = C / A

data = np.loadtxt(f"./Data-20262506/{File_index}.dat")

V_GS = data[:, 0]
I_DS = data[:, 2]
V_DS = data[:, 3]
# V_C = 0.5 * (data[:, 4] + data[:, 5])
V_12 = data[:, 6]
sigma = -data[:, 7]

plt.plot(
    -V_GS,
    sigma * 1e6,
    color='red',
    )

plt.xlabel(r"Gate Voltage -$V_\mathrm{G4}$ (V)")
plt.ylabel(r"Conductance $\sigma$ ($\mu$S/sq)")
plt.xlim(30, 50)
plt.ylim(0, 1)
plt.title("Conductance vs. Gate Voltage")
plt.show()


mu_var = -sigma/Ci/V_GS * 1e4

plt.plot(
    -V_GS,
    mu_var,
    color='red',
    )


plt.xlabel(r"Gate Voltage -$V_\mathrm{G4}$ (V)")
plt.ylabel(r"Mobility ($\mu$ (cm$^2$/Vs))")
plt.title("Mobility vs. Gate Voltage")
plt.xlim(30, 50)
plt.ylim(0, 5)
# plt.legend()
# plt.savefig("mu_cold.eps", format = 'eps')
plt.show()

plt.plot(
    -V_GS,
    -V_DS,
    color='red',
    )

plt.xlabel(r"Gate Voltage -$V_{\mathrm{G4}}$ (V)")
plt.ylabel(r"Drain Voltage -$V_{\mathrm{34}}$ (V)")
plt.title("V34 vs. Gate Voltage")
plt.xlim(30, 50)
plt.ylim(0,20)
# plt.legend()
# plt.savefig("V34_cold.eps", format = 'eps')
plt.show()

plt.plot(
    -V_GS,
    V_12,
    color='red',
    )


plt.xlabel(r"Gate Voltage -$V_\mathrm{G4}$ (V)")
plt.ylabel(r"VDP Voltage -$V_\mathrm{12}$ (V)")
plt.title("V12 vs. Gate Voltage")
plt.xlim(30, 50)
plt.ylim(0,1)
# plt.legend()
# plt.savefig("V12_cold.eps", format = 'eps')
plt.show()