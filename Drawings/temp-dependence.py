import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Custom settings
plt.style.use('classic')
plt.rcParams.update({
    'text.usetex': True,
    'text.latex.preamble': r'\usepackage{amsmath}\usepackage{siunitx}',
    'figure.dpi': 100,
    'figure.figsize': (10, 6),
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.linewidth': 2,
    'axes.labelsize': 15,
    'axes.labelcolor': 'black',
    'savefig.facecolor': 'white',
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial'],
    'mathtext.fontset': 'cm',
    "figure.constrained_layout.use": True,
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
plt.semilogy(1/T, mu_band, label='Band Transport', color='blue', lw = 2)
plt.semilogy(1/T, mu_hopping, label='Hopping Transport', color='red', lw = 2)
plt.xlabel(r'Inverse Temperature $T^{-1}$', fontsize=18)
plt.ylabel(r'Mobility $\mu$', fontsize=18)
plt.title('Temperature Dependence of Mobility', fontsize=18)
plt.legend()
plt.tick_params(labelbottom=False, labelleft=False)

plt.text(0.0075, 5e-6, r'$\propto T^{-3/2}$', color='blue', fontsize=18)
plt.text(0.0075, 2e-7, r'$\propto e^{-E_a/(k_\mathrm{B} T)}$', color='red', fontsize=18)
plt.xlim(0.0025, 0.01)
plt.ylim(1e-9, 1e-4)
plt.savefig('temp-dependence.eps', format='eps')
plt.show()
