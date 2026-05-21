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


E_V = -3*E_T  # Valence band edge energy
E_g = 4*E_T  # Band gap energy
E_L = E_V + E_g  # Conduction band edge energy
m_e = 1.0  # Effective mass of electrons
m_h = 1.0  # Effective mass of holes

E_F = 0  # Fermi energy at mid-gap



E = np.linspace(-10, 10, 2000)  # Energy range

f_n = 1 / (np.exp(beta * (E - E_F)) + 1)  # Fermi-Dirac distribution
f_p = 1 - f_n  # Hole distribution function (1 - f_n)

D_n =(m_e**(3/2) * np.sqrt(np.maximum(E - E_L, 0)))  # Density of states for electrons
D_p =(m_h**(3/2) * np.sqrt(np.maximum(E_V - E, 0)))  # Density of states for holes
D = D_n + D_p  # Total density of states

n_n = D_n * f_n
n_p = D_p * f_p
# Plotting
plt.figure(figsize=(6, 8))
plt.plot(n_n, E, label='Electron Density', color='blue', lw = 2)
plt.fill_betweenx(E, 0, n_n, color='blue', alpha=0.25)
plt.plot(n_p, E, label='Hole Density', color='red', lw = 2)
plt.fill_betweenx(E, 0, n_p, color='red', alpha=0.25)
# plt.plot(f_n, E, label='Electron Probability', color='blue', lw = 1.5, linestyle='--')
# plt.plot(f_p, E, label='Hole Probability', color='red', lw = 1.5, linestyle='--')
# plt.plot(D_n, E, label='Electron DOS', color='cyan', lw = 1, linestyle='--')
# plt.plot(D_p, E, label='Hole DOS', color='magenta', lw = 1, linestyle='--')
plt.axhline(E_V, color='black', linestyle='--')
plt.axhline(E_L, color='black', linestyle='--')
plt.axhline(E_F, color='black', linestyle='--')
plt.title('Electron and Hole Density Distributions', fontsize=18)
plt.xlim(0, 0.2)  # Set x-axis limits to focus on the density distributions
plt.ylim(np.min(E), np.max(E))  # Set y-axis limits to the energy range
plt.xlabel(r'Density of occupied states ($D(E) f(E)$)', fontsize=15)
plt.ylabel(r'Energy ($E$)', fontsize=15)
plt.xticks([])  # Remove x-axis ticks
plt.yticks([E_V, E_F, E_L], [r'$E_V$', r'$E_F$', r'$E_L$'])  # Custom y-axis ticks
plt.legend()
plt.savefig('doped_density.eps', format='eps', bbox_inches='tight')
plt.show()
