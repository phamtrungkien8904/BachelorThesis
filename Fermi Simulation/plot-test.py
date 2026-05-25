import numpy as np
import matplotlib.pyplot as plt

L = 5e-6  # Physical size of the domain in meters
N = 201
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

V = np.loadtxt("./Data-Export/schottky_Poti_01.dat")
p = np.loadtxt("./Data-Export/schottky_Dens_01.dat")/e + N_A

E = -np.gradient(V, dx)
dp_dx = np.gradient(p, dx)
J_drift = e*mu * p * E 
J_diffusion = -mu * e *V_T * dp_dx




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
ax2.set_ylabel('Hole Concentration (m^-3)')
ax2.set_xlim(0, L * 1e6)
ax2.set_ylim(0, np.max(p) * 1.5)

fig, (ax3, ax4) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

ax3.plot(x * 1e6, E, color='green', lw=2)
ax3.axhline(0, color='black', linestyle='--')
ax3.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='--')
ax3.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='--')
ax3.set_ylabel('Electric Field (V/m)')

ax4.plot(x * 1e6, dp_dx, color='purple', lw=2)
ax4.axhline(0, color='black', linestyle='--')
ax4.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='--')
ax4.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='--')
ax4.set_xlabel('Position (um)')
ax4.set_ylabel('dp/dx (m$^{-4}$)')
ax4.set_xlim(0, L * 1e6)



fig.tight_layout()
plt.show()

plt.plot(x * 1e6, J_drift, color='orange', lw=2)
plt.plot(x * 1e6, J_diffusion, color='purple', lw=2)
plt.plot(x * 1e6, J_drift + J_diffusion, color='brown', lw=2)
plt.ylabel('Current Density (A/m$^2$)')
plt.xlabel('Position (um)')
plt.xlim(0, L * 1e6)
plt.ylim(-1,1)
plt.legend(['Drift Current Density', 'Diffusion Current Density', 'Total Current Density'])
plt.title('Total Current Density Profile')
plt.show()