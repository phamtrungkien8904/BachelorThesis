import numpy as np
import matplotlib.pyplot as plt

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
    # 'figure.figsize': (10/2.54, 6/2.54),  # 10x6 cm in inches (1 figure per line)
    'figure.figsize': (6/2.54, 8/2.54),  # 10x6 cm in inches (2 figures per line)
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

# Constants
k_B = 1.0  # Boltzmann constant
T = 1.0  # Temperature
beta = 1/(k_B * T)  # 1/(k_B * T)
E_T = 1/beta  # Thermal energy


E_V = -2*E_T  # Valence band edge energy
E_g = 4*E_T  # Band gap energy
E_L = E_V + E_g  # Conduction band edge energy
m_e = 1.0  # Effective mass of electrons
m_h = 1.0  # Effective mass of holes

E_F = 0   # Fermi energy at mid-gap



E = np.linspace(-10, 10, 2000)  # Energy range

f_n = 1 / (np.exp(beta * (E - E_F)) + 1)  # Fermi-Dirac distribution
f_p = 1 - f_n  # Hole distribution function (1 - f_n)

D_n =(m_e**(3/2) * np.sqrt(np.maximum(E - E_L, 0)))  # Density of states for electrons
D_p =(m_h**(3/2) * np.sqrt(np.maximum(E_V - E, 0)))  # Density of states for holes
D = D_n + D_p  # Total density of states

n_n = D_n * f_n
n_p = D_p * f_p
# Plotting
plt.plot(n_n, E, label='Electron Density', color='blue', lw = 2)
plt.fill_betweenx(E, 0, n_n, color='#8fbce6')
plt.plot(n_p, E, label='Hole Density', color='red', lw = 2)
plt.fill_betweenx(E, 0, n_p, color='#f2a6a6')
plt.text(0.01, E_F + 3, r'$n_i$', color='black', ha='center', va='center')
plt.text(0.01, E_F - 3, r'$n_i$', color='black', ha='center', va='center')
# plt.plot(f_n, E, label='Electron Probability', color='blue', lw = 1.5, linestyle='--')
# plt.plot(f_p, E, label='Hole Probability', color='red', lw = 1.5, linestyle='--')
# plt.plot(D_n, E, label='Electron DOS', color='cyan', lw = 1, linestyle='--')
# plt.plot(D_p, E, label='Hole DOS', color='magenta', lw = 1, linestyle='--')
plt.axhline(E_V, color='black', linestyle='--')
plt.axhline(E_L, color='black', linestyle='--')
plt.axhline(E_F, color='black', linestyle='--')
plt.title('Electron and Hole Density Distributions\n (Intrinsic Semiconductor)')
plt.xlim(0, 0.2)  # Set x-axis limits to focus on the density distributions
plt.ylim(np.min(E), np.max(E))  # Set y-axis limits to the energy range
plt.xlabel(r'Density of occupied states ($D(E) f(E)$)')
plt.ylabel(r'Energy ($E$)')
plt.xticks([])  # Remove x-axis ticks
plt.yticks([E_V, E_F, E_L], [r'$E_V$', r'$E_F$', r'$E_L$'])  # Custom y-axis ticks
plt.legend()
plt.savefig('intrinsic_density.eps', format='eps')
plt.show()
