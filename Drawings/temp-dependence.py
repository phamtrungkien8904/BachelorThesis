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
    'figure.figsize': (10/2.54, 6/2.54),  # 10x6 cm in inches (1 figure per line)
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




# Temperature dependence of mobility (Band transport and hopping transport)

T = np.linspace(100, 400, 1000)  # Temperature range from 100K to 400K
# Band transport: μ ~ T^(-3/2)
mu_band = 1e-6 * (T / 300) ** (-1.5)
# Hopping transport: μ ~ exp(-Ea/kT)
Ea = 0.1  # Activation energy in eV
k_B = 8.617e-5  # Boltzmann constant in eV/K
mu_hopping = 1e-3 * np.exp(-Ea / (k_B * T))

plt.figure()
plt.semilogy(1/T, mu_band, label='Band Transport', color='blue')
plt.semilogy(1/T, mu_hopping, label='Hopping Transport', color='red')
plt.xlabel(r'Inverse Temperature $T^{-1}$')
plt.ylabel(r'Log Mobility $\log(\mu)$')
plt.title('Temperature Dependence of Mobility')
plt.legend()
plt.tick_params(labelbottom=False, labelleft=False)

plt.text(0.0075, 5e-6, r'$\propto T^{-3/2}$', color='blue')
plt.text(0.0075, 2e-7, r'$\propto e^{-E_a/(k_\mathrm{B} T)}$', color='red')
plt.xlim(0.0025, 0.01)
plt.ylim(1e-9, 1e-4)
plt.savefig('temp-dependence.eps', format='eps')
plt.show()
