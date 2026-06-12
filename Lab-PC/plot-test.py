import numpy as np
import matplotlib.pyplot as plt

plt.style.use('classic')
plt.rcParams.update({
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

    'savefig.bbox': 'tight',
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

L = 100e-9 # Physical size of the domain in meters
N = 1001
x = np.linspace(0, L, N)
dx = x[1] - x[0]
contact_size = 0.1
contact_width = int(contact_size * N) + 1
# Physical constants
k_B = 1.380649e-23  # Boltzmann constant in J/K
T = 300
e = 1.602176634e-19  # Elementary charge in Coulombs
epsilon = 3 * 8.854187817e-12  # Permittivity of semiconductor (epsilon_r * epsilon_0) in F/m
mu = 1e-4  # Mobility in m^2/(V*s)

V_T = k_B * T / e
V_bi = V_T * 5  # Built-in potential in volts
V_ext = 6*V_T  # External voltage in volts (Reverse: V_ext < 0, Forward: V_ext > 0)
V_tot = V_bi - V_ext  # Effective built-in potential in volts
N_A = 1e18  # Acceptor concentration in m^-3

V = np.loadtxt("./Data-Export/Schottky/schottky_Poti_01.dat")
p = np.loadtxt("./Data-Export/Schottky/schottky_Dens_01.dat")/e + N_A




fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

ax1.plot(x * 1e6, V, color='blue', lw=2)
ax1.axhline(0, color='black', linestyle='--')
ax1.axhline(-V_tot, color='black', linestyle='--')
ax1.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='--')
ax1.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='--')
ax1.set_ylabel('Potential (V)')
ax1.set_title('Schottky Barrier (p-type) Simulation', fontsize=18)
ax1.set_xlim(0, L * 1e6)
ax1.set_ylim(-0.05, 0.05)

ax2.plot(x * 1e6, p, color='red', lw=2)
ax2.axhline(N_A, color='black', linestyle='--')
ax2.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='--')
ax2.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='--')
ax2.set_xlabel('Position (um)')
ax2.set_ylabel('Net Charge Density (C/m^3)')
ax2.set_xlim(0, L * 1e6)
ax2.set_ylim(np.min(p) * 1.5, np.max(p) * 1.5)




fig.tight_layout()
plt.show()
