import numpy as np
import matplotlib.pyplot as plt

plt.style.use('classic')
plt.rcParams.update({
    'figure.dpi': 100,
    'figure.figsize': (8, 6),
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
V_bi = Vth * 2  # Built-in potential in volts
V_D = 0*Vth  # External voltage in volts (Reverse: V_ext < 0, Forward: V_ext > 0)
E_B = k_B * T * (np.log(N_v / N_A) - (V_bi - V_D) / Vth)  # [J]
p_left = N_v * np.exp(-(E_B - e * V_D) / (k_B * T))
E_g = 10*Vth*e


V = np.loadtxt("./Data-Export/Ohmic/ohmic_Poti_01.dat")
F = np.loadtxt("./Data-Export/Ohmic/ohmic_Fermi_01.dat")
rho = np.loadtxt("./Data-Export/Ohmic/ohmic_Dens_01.dat")
p = rho/e + N_A





fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

ax1.plot(x[contact_width:-contact_width] * 1e6, -V[contact_width:-contact_width], color='red', lw=2)
ax1.plot(x * 1e6, F, color='k', ls='--')
ax1.plot(x[contact_width:-contact_width] * 1e6, -V[contact_width:-contact_width] + E_g / e, color='blue', lw=2, ls='-')
# ax1.axhline(0, color='black', linestyle='--')
# ax1.axhline(V_bi, color='black', linestyle='--')
ax1.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='-', lw = 2)
ax1.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='-', lw = 2)
ax1.set_ylabel('Energy')
# ax1.set_title('Schottky Barrier (p-type) Simulation', fontsize=18)
ax1.set_xlim(0, L * 1e6*0.5)
ax1.set_ylim(-0.2, 0.4)
ax1.set_xticks([])
ax1.set_yticks([])

# place energy labels on the right, just above each curve
xlim = ax1.get_xlim()
x_label = xlim[1] - 0.02 * (xlim[1] - xlim[0])
y_EFS = np.interp(x_label, x * 1e6, F)
y_EV = np.interp(x_label, x * 1e6, -V)
y_EC = np.interp(x_label, x * 1e6, -V + E_g / e)
y_E0 = np.interp(x_label, x * 1e6, F - E_B / e)
ax1.text(x_label, y_EFS + 0.01, r'$E_{FS}$', color='black', fontsize=14, ha='right', va='bottom')
ax1.text(x_label, y_EV + 0.01, r'$E_V$', color='red', fontsize=14, ha='right', va='bottom')
ax1.text(x_label, y_EC + 0.01, r'$E_C$', color='blue', fontsize=14, ha='right', va='bottom')
# ax1.plot(x[contact_width:contact_width + 300] * 1e6, F[contact_width:contact_width + 300] - E_B / e, color='black', ls='--')
# annotate metal Fermi level explanation near left contact
metal_x = (contact_width - 1) * dx * 1e6 - 0.13 * (xlim[1] - xlim[0])
metal_y = np.interp(metal_x, x * 1e6, F)
ax1.text(metal_x, metal_y + 0.01, r'$E_{FM}$',
         color='black', fontsize=14, ha='left', va='bottom')


# x_arrow_1 = x_label - 0.3 * (xlim[1] - xlim[0])
# x_arrow_2 = x_label - 0.8 * (xlim[1] - xlim[0])
# ax1.annotate('', xy=(x_arrow_1, y_EV), xytext=(x_arrow_1, y_E0),
#              arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
# ax1.text(x_arrow_1 + 0.04 * (xlim[1] - xlim[0]), (y_EV + y_E0) / 2, r'$eV_\text{bi}$', color='black', fontsize=14, ha='center', va='center')

# ax1.annotate('', xy=(x_arrow_2, metal_y), xytext=(x_arrow_2, y_EFS),
#              arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
# ax1.text(x_arrow_2 - 0.07 * (xlim[1] - xlim[0]), (metal_y + y_EFS) / 2, r'$eV_\text{ext} < 0$', color='black', fontsize=14, ha='center', va='center')


ax2.fill_between(x[contact_width:-contact_width] * 1e6, rho[contact_width:-contact_width], 0, color='#f2a6a6', zorder=1)
ax2.plot(x[contact_width:-contact_width] * 1e6, rho[contact_width:-contact_width], color='r', lw=2, zorder=2)
ax2.axhline(0, color='black',  linestyle='--')
ax2.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='-', lw = 2)
ax2.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='-', lw = 2)
zero_label_y = 0.02 * (np.max(rho) - np.min(rho))
ax2.text(x_label, zero_label_y, r'$0$', color='blue', fontsize=14, va='bottom')
ax2.set_ylabel('Net Charge Density')
ax2.set_xlim(0, L * 1e6*0.5)
ax2.set_ylim(-np.max(rho) * 1.5, np.max(rho) * 1.5)
ax2.set_xticks([])
ax2.set_yticks([])




fig.tight_layout()
plt.savefig("ohmic-00.eps", format='eps') 
plt.show()
