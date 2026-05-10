import numpy as np
import matplotlib.pyplot as plt

# Custom settings
plt.style.use('classic')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['figure.dpi'] = 100

# Constants
kT = 1.0  # Thermal energy (k_B * T)
beta = 1/kT  # 1/(k_B * T)
E_V = 0  # Valence band edge energy
E_g = 4  # Band gap energy
E_L = E_V + E_g  # Conduction band edge energy
E_F = (E_V + E_L) / 2 + 1 * E_g  # Fermi energy at mid-gap
# Fermi-Dirac distribution function

E = np.linspace(-20, 20, 400)  # Energy range
f_E = 1 / (np.exp(beta * (E - E_F)) + 1)  # Fermi-Dirac distribution

# Plotting
plt.figure(figsize=(8, 5))
plt.plot(E, f_E, label=r'$f(E) = \frac{1}{e^{\beta (E - E_F)} + 1}$', color='blue', lw = 2)
plt.title('Fermi-Dirac Distribution Function')
plt.xlabel('Energy (E)')
plt.ylabel('Occupation Probability (f(E))')
plt.axhline(0.5, color='k', linestyle='--')
plt.axvline(E_F, color='k', linestyle='--')
plt.axvline(E_V, color='red', linestyle='--', label='Valence Band (E_V)')
plt.axvline(E_L, color='green', linestyle='--', label='Conduction Band (E_L)')
plt.legend()
plt.xlim(-20, 20)
plt.ylim(-0.05, 1.05)
plt.show()
