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

data2 = np.loadtxt("./Data-20262606/02.dat")
data3 = np.loadtxt("./Data-20262606/03.dat")
data5 = np.loadtxt("./Data-20262606/05.dat")
data6 = np.loadtxt("./Data-20262606/06.dat")
data7 = np.loadtxt("./Data-20262606/07.dat")
data8 = np.loadtxt("./Data-20262606/08.dat")
data9 = np.loadtxt("./Data-20262606/09.dat")
data10 = np.loadtxt("./Data-20262606/10.dat")
data11 = np.loadtxt("./Data-20262606/11.dat")
data12 = np.loadtxt("./Data-20262606/12.dat")

data30 = np.loadtxt("./Data-20262506/02.dat")
data31 = np.loadtxt("./Data-20262506/11.dat")


C = 1.8e-9
A = 32e-6
Ci = C / A

dataset = [
    data2, 'Data 2', 'red',
    # data3, 'Data 3', 'lightgreen',
    # data5, 'Data 5', 'purple',
    # data6, 'Data 6', 'brown',
    # data7, 'Data 7', 'pink',
    # data8, 'Data 8', 'cyan',
    # data9, 'Data 9', 'green',
    # data10, 'Data 10', 'black',
    # data11, 'Data 11', 'magenta',
    data12, 'Data 12', 'blue',
    data30, 'Data 30', 'black',
    data31, 'Data 31', 'orange'
]


# dataset = [
#     data2, 'Data 2', 'red',
#     data11, 'Data 11', 'blue'
# ]


C = 1.8e-9
A = 32e-6
Ci = C / A




# Create a 2x2 figure
fig, axs = plt.subplots(2, 2, figsize=(7.5, 6.5))
fig.set_constrained_layout_pads(wspace=0.1, hspace=0.1)


# -----------------------
# (1) Conductance
# -----------------------
for data, label, color in zip(dataset[::3], dataset[1::3], dataset[2::3]):
    V_GS = data[:, 0]
    I_DS = data[:, 2]
    V_DS = data[:, 3]
    # V_C = 0.5 * (data[:, 4] + data[:, 5])
    V_12 = data[:, 6]
    sigma = -data[:, 7]
    mu_var = -sigma/Ci/V_GS * 1e4
    axs[0, 0].plot(-V_GS, sigma * 1e6, color=color, label=label)


axs[0, 0].set_xlabel(r"Gate Voltage -$V_\mathrm{G4}$ (V)")
axs[0, 0].set_ylabel(r"Conductance $\sigma$ ($\mu$S/sq)")
# axs[0, 0].set_title("Conductance vs. Gate Voltage")
axs[0, 0].set_xlim(35, 50)
axs[0, 0].set_ylim(0.0, 2.5)

# -----------------------
# (2) Mobility
# -----------------------
for data, label, color in zip(dataset[::3], dataset[1::3], dataset[2::3]):
    V_GS = data[:, 0]
    I_DS = data[:, 2]
    V_DS = data[:, 3]
    # V_C = 0.5 * (data[:, 4] + data[:, 5])
    V_12 = data[:, 6]
    sigma = -data[:, 7]
    mu_var = -sigma/Ci/V_GS * 1e4
    axs[0, 1].plot(-V_GS, mu_var, color=color, label=label)
axs[0, 1].set_xlabel(r"Gate Voltage -$V_\mathrm{G4}$ (V)")
axs[0, 1].set_ylabel(r"Mobility $\mu$ (cm$^2$/Vs)")
# axs[0, 1].set_title("Mobility vs. Gate Voltage")
axs[0, 1].set_xlim(35, 50)
axs[0, 1].set_ylim(0, 15)

# -----------------------
# (3) V34
# -----------------------
for data, label, color in zip(dataset[::3], dataset[1::3], dataset[2::3]):
    V_GS = data[:, 0]
    I_DS = data[:, 2]
    V_DS = data[:, 3]
    # V_C = 0.5 * (data[:, 4] + data[:, 5])
    V_12 = data[:, 6]
    sigma = -data[:, 7]
    mu_var = -sigma/Ci/V_GS * 1e4
    axs[1, 0].plot(-V_GS, -V_DS, color=color, label=label)

axs[1, 0].set_xlabel(r"Gate Voltage -$V_\mathrm{G4}$ (V)")
axs[1, 0].set_ylabel(r"Drain Voltage -$V_\mathrm{34}$ (V)")
# axs[1, 0].set_title("V34 vs. Gate Voltage")
axs[1, 0].set_xlim(35, 50)
axs[1, 0].set_ylim(6, 10)

# -----------------------
# (4) V12
# -----------------------
for data, label, color in zip(dataset[::3], dataset[1::3], dataset[2::3]):
    V_GS = data[:, 0]
    I_DS = data[:, 2]
    V_DS = data[:, 3]
    # V_C = 0.5 * (data[:, 4] + data[:, 5])
    V_12 = data[:, 6]
    sigma = -data[:, 7]
    mu_var = -sigma/Ci/V_GS * 1e4
    axs[1, 1].plot(-V_GS, V_12, color=color, label=label)

axs[1, 1].set_xlabel(r"Gate Voltage -$V_\mathrm{G4}$ (V)")
axs[1, 1].set_ylabel(r"VDP Voltage -$V_\mathrm{12}$ (V)")
# axs[1, 1].set_title("V12 vs. Gate Voltage")
axs[1, 1].set_xlim(35, 50)
axs[1, 1].set_ylim(0.0, 0.2)

# Optional: save figure
# plt.savefig("TripC12_full_2.eps", format='eps')
plt.savefig("TripC12_firstlast_3.eps", format='eps')

plt.show()