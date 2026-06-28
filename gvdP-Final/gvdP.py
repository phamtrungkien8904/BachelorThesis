import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Custom settings for python figures
plt.style.use('classic')

plt.rcParams.update({
    "text.usetex": True,
    'text.latex.preamble': r'''
    \usepackage[T1]{fontenc}
    \usepackage{lmodern}
    \usepackage[utf8]{inputenc}
    \usepackage{amsmath}
    \usepackage{amssymb}
    \usepackage{siunitx}
    \usepackage{sfmath}
    '''
})
plt.rcParams.update({
    # Figure settings
    'figure.dpi': 100,
    # 'figure.figsize': (10/2.54, 8/2.54),  # 10x6 cm in inches (1 figure per line)
    # 'figure.figsize': (8/2.54, 6/2.54),  # 10x6 cm in inches (2 figures per line)
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.linewidth': 1,
    'axes.labelsize': 10,
    'axes.titlesize': 10,
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
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,  

    # Legend
    'legend.frameon': False,
    'legend.title_fontsize': 10,
    'legend.fontsize': 10,
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

data1 = np.loadtxt("./gvdP-PS9/01.dat")
data2 = np.loadtxt("./gvdP-PS9/02.dat")
data3 = np.loadtxt("./gvdP-PS9/03.dat")

dataset =[
    data1, "-100", 3.07, -10.05, 'red', 'o',
    data2, "-200", 3.08, -10.22, 'blue', 's',
    data3, "-300", 3.09, -10.19, 'green', '^',
]

e = 1.60217662e-19
C = 2e-9
A = 32e-6
Ci = C / A
markevery = 4


# Create a 2x2 figure
fig, axs = plt.subplots(2, 2, figsize=(6.5, 5.5))
fig.set_constrained_layout_pads(wspace=0.1, hspace=0.1)


# -----------------------
# (1) Conductance
# -----------------------
for data, label, mu, V_T, color, marker in zip(dataset[::6], dataset[1::6], dataset[2::6], dataset[3::6], dataset[4::6], dataset[5::6]):
    V_G4 = data[:, 0]
    I_34 = data[:, 2]
    V_34 = data[:, 3]
    V_14 = data[:, 4]
    V_24 = data[:, 5]
    V_12 = data[:, 6]
    sigma = -np.log(2) / np.pi * I_34 / V_12
    V_C = 0.5 * (V_14 + V_24)
    V_del = V_G4 - V_C
    mu = -sigma / Ci / (V_del - V_T) * 1e4
    axs[0, 0].plot(-V_del, sigma * 1e6, color=color, label=label, marker=marker, markevery=markevery)


axs[0, 0].set_xlabel(r"Effective Gate Voltage $-(V_\mathrm{G4} - V_\mathrm{C})$ (V)")
axs[0, 0].set_ylabel(r"Conductance $\sigma$ ($\mu$S/sq)")
# axs[0, 0].set_title("Conductance vs. Gate Voltage")
axs[0, 0].legend(title=r"$I_\mathrm{34}$ (nA)")
axs[0, 0].set_xlim(15, 30)
axs[0, 0].set_ylim(0, 1)

# -----------------------
# (2) Mobility
# -----------------------
for data, label, mu, V_T, color, marker in zip(dataset[::6], dataset[1::6], dataset[2::6], dataset[3::6], dataset[4::6], dataset[5::6]):
    V_G4 = data[:, 0]
    I_34 = data[:, 2]
    V_34 = data[:, 3]
    V_14 = data[:, 4]
    V_24 = data[:, 5]
    V_12 = data[:, 6]
    sigma = -np.log(2) / np.pi * I_34 / V_12
    V_C = 0.5 * (V_14 + V_24)
    V_del = V_G4 - V_C
    mu = -sigma / Ci / (V_del - V_T) * 1e4
    axs[0, 1].plot(-V_del, mu, color=color, label=label, marker=marker, markevery=markevery)
axs[0, 1].set_xlabel(r"Effective Gate Voltage $-(V_\mathrm{G4} - V_\mathrm{C})$ (V)")
axs[0, 1].set_ylabel(r"Mobility $\mu$ (cm$^2$/Vs)")
# axs[0, 1].set_title("Mobility vs. Gate Voltage")
axs[0, 1].legend(title=r"$I_\mathrm{34}$ (nA)")
axs[0, 1].set_xlim(15, 30)
axs[0, 1].set_ylim(0, 10)

# -----------------------
# (3) V34
# -----------------------
for data, label, mu, V_T, color, marker in zip(dataset[::6], dataset[1::6], dataset[2::6], dataset[3::6], dataset[4::6], dataset[5::6]):
    V_G4 = data[:, 0]
    I_34 = data[:, 2]
    V_34 = data[:, 3]
    V_14 = data[:, 4]
    V_24 = data[:, 5]
    V_12 = data[:, 6]
    sigma = -np.log(2) / np.pi * I_34 / V_12
    V_C = 0.5 * (V_14 + V_24)
    V_del = V_G4 - V_C
    mu = -sigma / Ci / (V_del - V_T) * 1e4
    axs[1, 0].plot(-V_G4, -V_34, color=color, label=label, marker=marker, markevery=markevery)

axs[1, 0].set_xlabel(r"Gate Voltage -$V_\mathrm{G4}$ (V)")
axs[1, 0].set_ylabel(r"Drain Voltage -$V_\mathrm{34}$ (V)")
# axs[1, 0].set_title("V34 vs. Gate Voltage")
axs[1, 0].set_xlim(15, 30)
axs[1, 0].set_ylim(0, 25)
axs[1, 0].legend(title=r"$I_\mathrm{34}$ (nA)")

# -----------------------
# (4) V12
# -----------------------
for data, label, mu, V_T, color, marker in zip(dataset[::6], dataset[1::6], dataset[2::6], dataset[3::6], dataset[4::6], dataset[5::6]):
    V_G4 = data[:, 0]
    I_34 = data[:, 2]
    V_34 = data[:, 3]
    V_14 = data[:, 4]
    V_24 = data[:, 5]
    V_12 = data[:, 6]
    sigma = -np.log(2) / np.pi * I_34 / V_12
    V_C = 0.5 * (V_14 + V_24)
    V_del = V_G4 - V_C
    mu = -sigma / Ci / (V_del - V_T) * 1e4
    axs[1, 1].plot(-V_G4, V_12, color=color, label=label, marker=marker, markevery=markevery)

axs[1, 1].set_xlabel(r"Gate Voltage -$V_\mathrm{G4}$ (V)")
axs[1, 1].set_ylabel(r"VDP Voltage -$V_\mathrm{12}$ (V)")
# axs[1, 1].set_title("V12 vs. Gate Voltage")
axs[1, 1].legend(title=r"$I_\mathrm{34}$ (nA)")
axs[1, 1].set_xlim(15, 30)
axs[1, 1].set_ylim(0, 0.5)

plt.savefig("vdP-full.eps", format='eps')
plt.show()