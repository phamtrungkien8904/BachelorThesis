import numpy as np
import matplotlib.pyplot as plt

plt.style.use('classic')
plt.rcParams.update({
    'figure.dpi': 100,
    'figure.figsize': (12, 8),
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


# Semiconductor parameters
N_A = 5e23                 # acceptor density [m^-3]
N_v = 1e25                  # effective DOS [m^-3]
Vth = k_B * T / e
V_bi = Vth * 10  # Built-in potential in volts
V_D = 0*Vth  # External voltage in volts (Reverse: V_ext < 0, Forward: V_ext > 0)
E_B = k_B * T * (np.log(N_v / N_A) + V_bi / Vth)  # [J]
p_left = N_v * np.exp(-(E_B - e * V_D) / (k_B * T))
E_g = 20*Vth*e


V = np.loadtxt("./Data-Export/Schottky/schottky_Poti_01.dat")
F = np.loadtxt("./Data-Export/Schottky/schottky_Fermi_01.dat")
rho = np.loadtxt("./Data-Export/Schottky/schottky_Dens_01.dat")
p = rho/e + N_A




fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

ax1.plot(x[contact_width:-contact_width] * 1e6, -V[contact_width:-contact_width], color='red', lw=2)
ax1.plot(x * 1e6, F, color='k', lw=2, ls='--')
ax1.plot(x[contact_width:-contact_width] * 1e6, -V[contact_width:-contact_width] + E_g / e, color='blue', lw=2, ls='-')
# ax1.axhline(0, color='black', linestyle='--')
# ax1.axhline(V_bi, color='black', linestyle='--')
ax1.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='-', lw = 2)
ax1.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='-', lw = 2)
ax1.set_ylabel('Energy (eV)')
ax1.set_title('Schottky Barrier (p-type) Simulation', fontsize=18)
ax1.set_xlim(0, L * 1e6/2)
ax1.set_ylim(-0.2, 1.0)
ax1.set_xticks([])
ax1.set_yticks([])

# place energy labels on the right, just above each curve
xlim = ax1.get_xlim()
x_label = xlim[1] - 0.02 * (xlim[1] - xlim[0])
y_EF = np.interp(x_label, x * 1e6, F)
y_EV = np.interp(x_label, x * 1e6, -V)
y_EC = np.interp(x_label, x * 1e6, -V + E_g / e)
ax1.text(x_label, y_EF + 0.03, r'$E_F$', color='black', fontsize=14, ha='right', va='bottom')
ax1.text(x_label, y_EV - 0.1, r'$E_V$', color='red', fontsize=14, ha='right', va='bottom')
ax1.text(x_label, y_EC + 0.03, r'$E_C$', color='blue', fontsize=14, ha='right', va='bottom')

# Visualize electrons as blue spheres near the interface inside the semiconductor
electron_x = np.array([0.0105, 0.0115, 0.0125, 0.0135, 0.0105, 0.0115, 0.0125, 0.0105]) # x-coordinates for electrons (in micrometers)
electron_y = np.array([0.74, 0.70, 0.74, 0.70, 0.66, 0.62, 0.66, 0.58])  # y-coordinates for electrons (fixed)
ax1.scatter(electron_x, electron_y, s=180, c='blue', edgecolors='navy', linewidths=1.2, zorder=5)
# draw a minus sign in the middle of each sphere
minus_half = 0.0001
for xi, yi in zip(electron_x, electron_y):
    ax1.plot([xi - minus_half, xi + minus_half], [yi, yi], color='white', lw=2.5, zorder=6, solid_capstyle='round')



# Visualize holes as red spheres near the interface inside the semiconductor
hole_x = np.array([0.0175, 0.0185, 0.0195, 0.0205, 0.0215]) + 0.02 # x-coordinates for holes (in micrometers)
hole_y = np.ones(5) * 0.2  # y-coordinates for holes (fixed)
ax1.scatter(hole_x, hole_y, s=180, c='red', edgecolors='darkred', linewidths=1.2, zorder=5)

# draw a plus sign in the middle of each sphere (use a scatter '+' marker for visibility)
ax1.scatter(hole_x, hole_y, marker='+', c='white', s=100, linewidths=2.5, zorder=6)

ax2.fill_between(x[contact_width:-contact_width] * 1e6, rho[contact_width:-contact_width], 0, color='#9ecae1', zorder=1)
ax2.plot(x[contact_width:-contact_width] * 1e6, rho[contact_width:-contact_width], color='b', lw=2, zorder=2)
ax2.axhline(0, color='black', lw = 2, linestyle='--')
ax2.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='-', lw = 2)
ax2.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='-', lw = 2)
zero_label_y = 0.02 * (np.max(rho) - np.min(rho))
ax2.text(x_label, zero_label_y, r'$0$', color='blue', fontsize=14, va='bottom')
ax2.set_ylabel('Net Charge Density (C/m^3)')
ax2.set_xlim(0, L * 1e6/2)
ax2.set_ylim(np.min(rho) * 1.5, -np.min(rho) * 1.5)
ax2.set_xticks([])
ax2.set_yticks([])




fig.tight_layout()
plt.show()
