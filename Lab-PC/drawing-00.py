import numpy as np
import matplotlib.pyplot as plt

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
    'figure.figsize': (8/2.54, 6/2.54),  
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
    # 'mathtext.fontset': 'cm',
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
V_D = 0*Vth  # External voltage in volts (Reverse: V_ext < 0, Forward: V_ext > 0)
E_B = k_B * T * (np.log(N_v / N_A) + V_bi / Vth)  # [J]
p_left = N_v * np.exp(-(E_B - e * V_D) / (k_B * T))
E_g = 20*Vth*e


V = np.loadtxt("./Data-Export/Schottky/schottky_Poti_01.dat")
F = np.loadtxt("./Data-Export/Schottky/schottky_Fermi_01.dat")
rho = np.loadtxt("./Data-Export/Schottky/schottky_Dens_01.dat")
p = rho/e + N_A




fig, ax = plt.subplots(1, 1)

ax.plot(x[contact_width:-contact_width] * 1e6, -V[contact_width:-contact_width], color='red', lw=1.5)
ax.plot(x * 1e6, F, color='k', lw=1, ls='--')
ax.plot(x[contact_width:-contact_width] * 1e6, -V[contact_width:-contact_width] + E_g / e, color='blue', lw=1.5, ls='-')
ax.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='-', lw = 1)
ax.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='-', lw = 1)
ax.text(0.028 * L * 1e6, -0.15 , 'Metal', color='black', fontsize=8, ha='left', va='bottom')
ax.text(0.24 * L * 1e6, -0.15 , 'Semiconductor', color='black', fontsize=8, ha='left', va='bottom')
ax.set_ylabel('')
# ax.set_title('Schottky Barrier (p-type) Simulation', fontsize=18)
ax.set_xlim(0, L * 1e6/2)
ax.set_ylim(-0.2, 1.0)
ax.set_xticks([])
ax.set_yticks([])
# hide axis lines, ticks and labels
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# place energy labels on the right, just above each curve
xlim = ax.get_xlim()
x_label = xlim[1] - 0.02 * (xlim[1] - xlim[0])
y_EF = np.interp(x_label, x * 1e6, F)
y_EV = np.interp(x_label, x * 1e6, -V)
y_EC = np.interp(x_label, x * 1e6, -V + E_g / e)
y_E0 = np.interp(x_label, x * 1e6, F - E_B / e)
ax.text(x_label, y_EF + 0.01, r'$E_F$', color='black', fontsize=8, ha='right', va='bottom')
ax.text(x_label, y_EV - 0.07, r'$E_V$', color='red', fontsize=8, ha='right', va='bottom')
ax.text(x_label, y_EC + 0.01, r'$E_C$', color='blue', fontsize=8, ha='right', va='bottom')

# Visualize electrons as blue spheres near the interface inside the semiconductor
electron_x = 1.3*np.array([0.0105, 0.0115, 0.0125, 0.0135, 0.0105, 0.0115, 0.0125, 0.0105, 0.0145]) - 0.003 # x-coordinates for electrons (in micrometers)
electron_y = np.array([0.74, 0.70, 0.74, 0.70, 0.66, 0.62, 0.66, 0.58, 0.74])  # y-coordinates for electrons (fixed)
ax.scatter(electron_x, electron_y, s=40, c='blue', edgecolors='navy', linewidths=1, zorder=2)
# draw a minus sign in the middle of each sphere
minus_half = 0.0002
for xi, yi in zip(electron_x, electron_y):
    ax.plot([xi - minus_half, xi + minus_half], [yi, yi], color='white', lw=1, zorder=2, solid_capstyle='round')



# Visualize holes as red spheres near the interface inside the semiconductor
hole_x = np.array([0.0175, 0.0195, 0.0215, 0.0235, 0.0255]) + 0.02 # x-coordinates for holes (in micrometers)
hole_y = np.ones(5) * 0.2  # y-coordinates for holes (fixed)
ax.scatter(hole_x, hole_y, s=40, c='red', edgecolors='darkred', linewidths=1, zorder=2)

# draw a plus sign in the middle of each sphere (use a scatter '+' marker for visibility)
ax.scatter(hole_x, hole_y, marker='+', c='white', s=20, linewidths=1, zorder=2)


x_arrow_1 = x_label - 0.4 * (xlim[1] - xlim[0])
x_arrow_2 = x_label - 0.85 * (xlim[1] - xlim[0])
# x_arrow_2 = x_label - 0.8 * (xlim[1] - xlim[0])
ax.annotate('', xy=(x_arrow_1, y_EV), xytext=(x_arrow_1, y_E0),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1))
ax.text(x_arrow_1 + 0.05 * (xlim[1] - xlim[0]), (y_EV + y_E0) / 2, r'$e V_\mathrm{bi} $', color='black', fontsize=8, ha='center', va='center')
ax.plot(x[contact_width-50:contact_width + 300] * 1e6, F[contact_width-50:contact_width + 300] - E_B / e, color='black', ls='--')


ax.annotate('', xy=(x_arrow_2, y_EF), xytext=(x_arrow_2, y_E0),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1))
ax.text(x_arrow_2 - 0.05 * (xlim[1] - xlim[0]), (y_EF + y_E0) / 2, r'$e \phi_\mathrm{B} $', color='black', fontsize=8, ha='center', va='center')


plt.savefig('Schottky-after-contact.eps', format='eps')
plt.show()
