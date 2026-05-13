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
kT = 1  # Thermal energy (k_B * T)
beta = 1/kT  # 1/(k_B * T)

E_V = 0  # Valence band edge energy
E_g = 4  # Band gap energy
E_L = E_V + E_g  # Conduction band edge energy
E_F = (E_V + E_L) / 2 + 1 * E_g  # Fermi energy at mid-gap


N_n = 1e21  # Effective density of states in the conduction band

# Fermi-Dirac distribution function
E = np.linspace(-20, 20, 400)  # Energy range
f_n = 1 / (np.exp(beta * (E - E_F)) + 1)  # Fermi-Dirac distribution
f_p = 1 - f_n  # Hole distribution function (1 - f_n)

# Density of states for a 3D semiconductor
D_n = np.zeros_like(E)
D_n[E >= E_L] = N_n * np.sqrt(E[E >= E_L] - E_L)

D_p = np.zeros_like(E)
D_p[E <= E_V] = N_n * np.sqrt(E_V - E[E <= E_V])


electron_density = D_n * f_n
n_n = np.trapezoid(electron_density, E)  # Electron concentration
print(f'Electron concentration (n): {n_n:.2e} cm^-3')

hole_density = D_p * f_p
n_p = np.trapezoid(hole_density, E)  # Hole concentration
print(f'Hole concentration (p): {n_p:.2e} cm^-3')


# Plot the potential distribution
fig, ax = plt.subplots(figsize=(8, 6))


# Smooth visualization for the computed grid (does not modify simulation values)
image = ax.imshow(
    electron_density.reshape(1, -1),  # Reshape for imshow
    extent=[E.min(), E.max(), E.min(), E.max()],
    origin='lower',
    cmap='Greys',
    interpolation='bicubic', # 'nearest' for exact grid values, 'bicubic' for smooth visualization
    vmin=0,
    vmax=electron_density.max()
)

cbar = fig.colorbar(image, ax=ax)
cbar.set_label('Electron density contribution')


ax.axvline(E_L, color='k', linestyle='--', label='Conduction Band Edge (E_L)')
ax.axvline(E_V, color='k', linestyle='--', label='Valence Band Edge (E_V)')
ax.axvline(E_F, color='k', linestyle='--', label='Fermi Energy (E_F)')
ax.set_title('Electron Density in a Semiconductor')
ax.set_xlabel('Energy (E)')
ax.set_ylabel('Electron density contribution')
plt.show()

plt.plot(E, electron_density, label='Electron density contribution', color='blue', lw=2)
plt.plot(E, hole_density, label='Hole density contribution', color='red', lw=2)
plt.axvline(E_L, color='k', linestyle='--', label='Conduction Band Edge (E_L)')
plt.axvline(E_V, color='k', linestyle='--', label='Valence Band Edge (E_V)')
plt.axvline(E_F, color='k', linestyle='--', label='Fermi Energy (E_F)')
plt.title('Charge Density in a Semiconductor')
plt.xlabel('Energy (E)')
plt.ylabel('Density contribution')
plt.ylim(0, electron_density.max()*1.1)
plt.show()
