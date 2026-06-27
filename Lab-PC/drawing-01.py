import numpy as np
import matplotlib.pyplot as plt

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
    'figure.figsize': (8/2.54, 6/2.54),  # 10x6 cm in inches (1 figure per line)
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
V_D = 5*Vth  # External voltage in volts (Reverse: V_ext < 0, Forward: V_ext > 0)
E_B = k_B * T * (np.log(N_v / N_A) + (V_bi - V_D) / Vth)  # [J]
p_left = N_v * np.exp(-(E_B - e * V_D) / (k_B * T))
E_g = 20*Vth*e

# Load Data (Replace paths as needed for your machine)
V = np.loadtxt("./Data-Export/Schottky/schottky_Poti_02.dat")
F = np.loadtxt("./Data-Export/Schottky/schottky_Fermi_02.dat")
rho = np.loadtxt("./Data-Export/Schottky/schottky_Dens_02.dat")
p = rho/e + N_A

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# ----------------- AXIS 1 (Energy) -----------------
ax1.plot(x[contact_width:-contact_width] * 1e6, -V[contact_width:-contact_width], color='red', lw=1.5)
ax1.plot(x * 1e6, F, color='k', ls='--')
ax1.plot(x[contact_width:-contact_width] * 1e6, -V[contact_width:-contact_width] + E_g / e, color='blue', lw=1.5, ls='-')

ax1.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='-', lw=1)
ax1.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='-', lw=1)
ax1.set_ylabel('Energy')
ax1.set_xlim(0, L * 1e6/2)
ax1.set_ylim(-0.2, 1.0)

# Labels for Energy Levels
xlim = ax1.get_xlim()
x_label = xlim[1] - 0.02 * (xlim[1] - xlim[0])
y_EFS = np.interp(x_label, x * 1e6, F)
y_EV = np.interp(x_label, x * 1e6, -V)
y_EC = np.interp(x_label, x * 1e6, -V + E_g / e)
y_E0 = np.interp(x_label, x * 1e6, F - E_B / e)

ax1.text(x_label, y_EFS + 0.03, r'$E_\mathrm{Fs}$', color='black', fontsize=8, ha='right', va='bottom')
ax1.text(x_label, y_EV - 0.12, r'$E_\mathrm{V}$', color='red', fontsize=8, ha='right', va='bottom')
ax1.text(x_label, y_EC + 0.01, r'$E_\mathrm{C}$', color='blue', fontsize=8, ha='right', va='bottom')
ax1.plot(x[contact_width:contact_width + 300] * 1e6, F[contact_width:contact_width + 300] - E_B / e, color='black', ls='--')

metal_x = (contact_width - 1) * dx * 1e6 - 0.13 * (xlim[1] - xlim[0])
metal_y = np.interp(metal_x, x * 1e6, F)
ax1.text(metal_x, metal_y + 0.02, r'$E_\mathrm{Fm}$', color='black', fontsize=8, ha='left', va='bottom')

# Annotations (Arrows)
x_arrow_1 = x_label - 0.3 * (xlim[1] - xlim[0])
x_arrow_2 = x_label - 0.8 * (xlim[1] - xlim[0])
ax1.annotate('', xy=(x_arrow_1, y_EV), xytext=(x_arrow_1, y_E0),
             arrowprops=dict(arrowstyle='<->,head_width=0.2,head_length=0.2', color='black', lw=0.7, shrinkA=0, shrinkB=0))
ax1.text(x_arrow_1 + 0.12 * (xlim[1] - xlim[0]), (y_EV + y_E0) / 2, r'$e(V_\mathrm{bi} - V_\mathrm{ext})$', color='black', fontsize=8, ha='center', va='center')

ax1.annotate('', xy=(x_arrow_2, metal_y), xytext=(x_arrow_2, y_EFS),
             arrowprops=dict(arrowstyle='<->,head_width=0.2,head_length=0.2', color='black', lw=0.7, shrinkA=0, shrinkB=0))

ax1.text(x_arrow_2 - 0.1 * (xlim[1] - xlim[0]), (metal_y + y_EFS) / 2, r'$eV_\mathrm{ext} > 0$', color='black', fontsize=8, ha='center', va='center')


# ----------------- AXIS 2 (Charge) -----------------
ax2.fill_between(x[contact_width:-contact_width] * 1e6, rho[contact_width:-contact_width], 0, color='#9ecae1', zorder=1)
ax2.plot(x[contact_width:-contact_width] * 1e6, rho[contact_width:-contact_width], color='b', lw=1, zorder=2)
ax2.axhline(0, color='black',  linestyle='--')
ax2.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='-', lw=1)
ax2.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='-', lw=1)

zero_label_y = 0.02 * (np.max(rho) - np.min(rho))
ax2.text(x_label, zero_label_y, r'$0$', color='blue', fontsize=8, va='bottom')
ax2.set_ylabel('Net Charge Density')
ax2.set_xlim(0, L * 1e6/2)
ax2.set_ylim(np.min(rho) * 1.5, -np.min(rho) * 1.5)


# ----------------- HIDE AXIS BORDERS & TICKS -----------------
for ax in [ax1, ax2]:
    # Stop layout text rendering
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False)
    
    # Target frame components individually to defeat sharex and rcParams
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)


plt.savefig("schottky-01.eps", format='eps') 
plt.show()
