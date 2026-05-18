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
k_B = 1.0  # Boltzmann constant
T = 1.0  # Temperature
beta = 1/(k_B * T)  # 1/(k_B * T)
E_T = 1/beta  # Thermal energy


E_V = 1  # Valence band edge energy
E_g = 10*E_T  # Band gap energy
E_L = E_V + E_g  # Conduction band edge energy
m_e = 1.0  # Effective mass of electrons
m_h = 2.0  # Effective mass of holes

E_F = (E_V + E_L) / 2 + 0.75 * E_T * np.log(m_h/m_e)  # Fermi energy at mid-gap



E = np.linspace(-20, 20, 400)  # Energy range

f_n = 1 / (np.exp(beta * (E - E_F)) + 1)  # Fermi-Dirac distribution
f_p = 1 - f_n  # Hole distribution function (1 - f_n)

D_n = (m_e**(3/2) * np.sqrt(np.maximum(E - E_L, 0)))  # Density of states for electrons
D_p = (m_h**(3/2) * np.sqrt(np.maximum(E_V - E, 0)))  # Density of states for holes
D = D_n + D_p  # Total density of states

n_n = D_n * f_n
n_p = D_p * f_p
# Plotting
plt.figure(figsize=(8, 6))
plt.plot(n_n, E, label='Electron Density', color='blue', lw = 2)
plt.plot(n_p, E, label='Hole Density', color='red', lw = 2)
plt.axhline(E_V, color='black', linestyle='--', label='Valence Band Edge')
plt.axhline(E_L, color='black', linestyle='--', label='Conduction Band Edge')
plt.axhline(E_F, color='black', linestyle='--', label='Fermi Energy')
plt.title('Electron and Hole Density Distributions')
plt.xlabel(r'Density of occupied states ($D(E) f(E)$)')
plt.ylabel(r'Energy ($E$)')
# plt.legend()
plt.show()
