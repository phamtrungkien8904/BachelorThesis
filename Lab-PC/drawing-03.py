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





fig, ax = plt.subplots(1, 1)

space = 100
ax.plot(x[contact_width+space:-contact_width] * 1e6, -V[contact_width]*np.ones_like(x[contact_width+space:-contact_width]), color='red', lw=1.5)
ax.plot(x[:contact_width] * 1e6, F[:contact_width], color='k', lw=1, ls='--')
ax.plot(x[contact_width+space:]*1e6, F[contact_width+space:] - V_bi, color='k', lw=1, ls='--')
ax.plot(x[contact_width+space:-contact_width] * 1e6, -V[contact_width]*np.ones_like(x[contact_width+space:-contact_width]) + E_g / e, color='blue', lw=1.5, ls='-')
ax.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='-', lw = 1)
ax.axvline((contact_width +space-1) * dx * 1e6, color='black', linestyle='-', lw = 1)
ax.axhline(1.0, color='black', linestyle='--')
ax.text(0.12 * L * 1e6, 0.94 , 'Vacuum', color='black', fontsize=8, ha='left', va='bottom')
ax.text(0.03 * L * 1e6, -0.15 , 'Metal', color='black', fontsize=8, ha='left', va='bottom')
ax.text(0.3 * L * 1e6, -0.15 , 'Semiconductor', color='black', fontsize=8, ha='left', va='bottom')


ax.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='-', lw = 1)
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
y_vac = np.interp(x_label, x * 1e6, 1.0*np.ones_like(x))
y_EF = np.interp(x_label, x * 1e6, F)
y_EV = np.interp(x_label, x[contact_width:-contact_width] * 1e6, -V[contact_width]*np.ones_like(x[contact_width:-contact_width]))
y_EC = np.interp(x_label, x[contact_width:-contact_width] * 1e6, -V[contact_width]*np.ones_like(x[contact_width:-contact_width]) + E_g / e)
y_E0 = np.interp(x_label, x * 1e6, F - E_B / e)
ax.text(x_label, y_EF - 0.25, r'$E_\mathrm{Fs}$', color='black', fontsize=8, ha='right', va='bottom')
ax.text(x_label, y_EV - 0.07, r'$E_\mathrm{V}$', color='red', fontsize=8, ha='right', va='bottom')
ax.text(x_label, y_EC + 0.01, r'$E_\mathrm{C}$', color='blue', fontsize=8, ha='right', va='bottom')


x_arrow_1 = x_label - 0.1 * (xlim[1] - xlim[0])
x_arrow_2 = x_label - 0.5 * (xlim[1] - xlim[0])
x_arrow_3 = x_label - 0.85 * (xlim[1] - xlim[0])
x_arrow_4 = x_label - 0.35 * (xlim[1] - xlim[0])
ax.annotate('', xy=(x_arrow_1, y_EV), xytext=(x_arrow_1, y_EC),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1))
ax.text(x_arrow_1 + 0.03 * (xlim[1] - xlim[0]), (y_EV + y_EC) / 2, r'$E_\mathrm{g} $', color='black', fontsize=8, ha='center', va='center')

ax.annotate('', xy=(x_arrow_2, y_vac), xytext=(x_arrow_2, y_EC),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1))
ax.text(x_arrow_2 + 0.03 * (xlim[1] - xlim[0]), (y_vac + y_EC) / 2, r'$e\chi$', color='black', fontsize=8, ha='center', va='center')
ax.annotate('', xy=(x_arrow_3, y_vac), xytext=(x_arrow_3, y_EF),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1))
ax.text(x_arrow_3 - 0.05 * (xlim[1] - xlim[0]), (y_vac + y_EF) / 2, r'$e\phi_\mathrm{m}$', color='black', fontsize=8, ha='center', va='center')
ax.text(x_arrow_3 - 0.05 * (xlim[1] - xlim[0]), y_EF + 0.05, r'$E_\mathrm{Fm}$', color='black', fontsize=8, ha='center', va='center')


ax.annotate('', xy=(x_arrow_4, y_vac), xytext=(x_arrow_4, y_E0),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1))
ax.text(x_arrow_4 + 0.03 * (xlim[1] - xlim[0]), (y_vac + y_E0 - 0.05) / 2, r'$e\phi_\mathrm{s}$', color='black', fontsize=8, ha='center', va='center')

# ax.plot(x[contact_width-50:contact_width + 300] * 1e6, F[contact_width-50:contact_width + 300] - E_B / e, color='black', ls='--')


# ax.annotate('', xy=(x_arrow_2, y_EF), xytext=(x_arrow_2, y_E0),
#              arrowprops=dict(arrowstyle='<->', color='black', lw=1))
# ax.text(x_arrow_2 - 0.03 * (xlim[1] - xlim[0]), (y_EF + y_E0) / 2, r'$e \phi_\text{B} $', color='black', fontsize=18, ha='center', va='center')

plt.savefig('Schottky-before-contact.eps', format='eps')

plt.show()
