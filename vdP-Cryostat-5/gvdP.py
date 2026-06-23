import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# Custom settings
plt.style.use('classic')
plt.rcParams.update({
    # "text.usetex": True,
    # 'text.latex.preamble': r'\usepackage{amsmath}',
    'figure.dpi': 100,
    'figure.figsize': (10, 6),
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.linewidth': 2,
    'axes.labelsize': 18,
    'axes.titlesize': 20,
    'axes.labelcolor': 'black',
    'savefig.facecolor': 'white',
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial'],
    'mathtext.fontset': 'cm',
    'figure.constrained_layout.use': True,

    # Ticks
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 8,
    "ytick.major.size": 8,
    "xtick.major.width": 2,
    "ytick.major.width": 2,
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "xtick.minor.size": 4,
    "ytick.minor.size": 4,
    "xtick.minor.width": 1.5,
    "ytick.minor.width": 1.5,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,  
})

C = 1.8e-9
A = 32e-6
Ci = C / A

# data = np.loadtxt("./Data-Mani/01.dat")
data1 = np.loadtxt("./gvdP/20260512003.dat") # PS
data2 = np.loadtxt("./gvdP/20260512004.dat") # Trip
data3 = np.loadtxt("./gvdP/20260512005.dat") # PaN

dataset = [
    data1, "PS", 3.24, -2.55, 'red', 's',
    data3, "PaN", 2.14, 7.14, 'black', '^',
    data2, "Trip C12", 1.90, -10.31, 'blue', 'o',
]

for data, label, mu, V_T, color, marker in zip(*[iter(dataset)]*6):
    V_GS = data[:, 0]
    I_DS = data[:, 2]
    V_DS = data[:, 3]
    V_C = 0.5 * (data[:, 4] + data[:, 5])
    V_12 = data[:, 6]
    sigma = -data[:, 7]
    V_del = -(V_GS - V_C)
    mu_var = sigma/Ci/(V_del - V_T)*10e3
    plt.plot(-V_GS, mu_var, label=label + r" ($\mu = %.2f$ cm$^2$/Vs)" % mu, color=color, marker=marker, ls='-', lw = 2, markevery=10, markeredgecolor="white", markeredgewidth=1, markersize=8)
    plt.axhline(mu, color=color, linestyle='--', linewidth=2)


plt.xlabel(r"Gate Voltage $-V_{G4}$ (V)")
plt.ylabel(r"Mobility $\mu$ (cm$^2$/Vs)")
plt.xlim(5, 50)
plt.ylim(0, 6)
plt.title("Mobility vs Gate Voltage")
plt.legend(frameon=False, numpoints=1, loc='upper right', fontsize=18)
plt.show()