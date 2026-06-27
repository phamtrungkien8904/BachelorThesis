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
    'figure.dpi': 300,
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

data = np.loadtxt("./Data-Mani/01.dat")


C = 1.8e-9
A = 32e-6
Ci = C / A
V_T = 19.30
mu =1.17
markevery = 4



# Create a 2x2 figure
fig, axs = plt.subplots(2, 2, figsize=(6.5, 5.5))
fig.set_constrained_layout_pads(wspace=0.1, hspace=0.1)


# -----------------------
# (1) Conductance
# -----------------------
V_GS = data[:, 0]
I_DS = data[:, 2]
V_DS = data[:, 3]
V_C = 0.5 * (data[:, 4] + data[:, 5])
V_12 = data[:, 6]
sigma = -data[:, 7]
V_del = -(V_GS - V_C)
mu_var = sigma/Ci/(V_del - V_T) * 1e4
axs[0, 0].plot(-V_GS, sigma * 1e6, color='red', marker='o', markevery=markevery, label='Conductance Data')
x = np.linspace(25, 40, 100)
y = mu * Ci * (x - V_T) * 1e-4
axs[0, 0].plot(x, y*1e6, color='blue', linestyle='--', label='Linear Fit')
axs[0, 0].legend()

axs[0, 0].set_xlabel(r"Gate Voltage -$V_\mathrm{G4}$ (V)")
axs[0, 0].set_ylabel(r"Conductance $\sigma$ ($\mu$S/sq)")
# axs[0, 0].set_title("Conductance vs. Gate Voltage")
axs[0, 0].set_xlim(25, 40)
# axs[0, 0].set_ylim(0.2, 0.8)

# -----------------------
# (2) Mobility
# -----------------------

axs[0, 1].plot(V_del, mu_var, color='red', marker='o', markevery=markevery, label='Mobility Data')
axs[0, 1].axhline(y=mu, color='blue', linestyle='--', label=rf'$\mu$ = {mu:.2f} cm$^2$/Vs')
axs[0, 1].legend()
axs[0, 1].set_xlabel(r"Gate Voltage -$V_\mathrm{G4}$ (V)")
axs[0, 1].set_ylabel(r"Mobility $\mu$ (cm$^2$/Vs)")
# axs[0, 1].set_title("Mobility vs. Gate Voltage")
axs[0, 1].set_xlim(25, 40)
axs[0, 1].set_ylim(0, 2)

# -----------------------
# (3) V34
# -----------------------
axs[1, 0].plot(V_del, -V_DS, color='red', marker='o', markevery=markevery)
axs[1, 0].set_xlabel(r"Gate Voltage -$V_\mathrm{G4}$ (V)")
axs[1, 0].set_ylabel(r"Drain Voltage -$V_\mathrm{34}$ (V)")
# axs[1, 0].set_title("V34 vs. Gate Voltage")
axs[1, 0].set_xlim(25, 40)
axs[1, 0].set_ylim(0, 10)

# -----------------------
# (4) V12
# -----------------------

axs[1, 1].plot(V_del, V_12, color='red', marker='o', markevery=markevery)
axs[1, 1].set_xlabel(r"Gate Voltage -$V_\mathrm{G4}$ (V)")
axs[1, 1].set_ylabel(r"VDP Voltage -$V_\mathrm{12}$ (V)")
# axs[1, 1].set_title("V12 vs. Gate Voltage")
axs[1, 1].set_xlim(25, 40)
axs[1, 1].set_ylim(0.0, 0.10)

# # Optional: save figure
plt.savefig("vdP-full.eps", format='eps')
# plt.savefig("TripC12_single_1.eps", format='eps')

plt.show()