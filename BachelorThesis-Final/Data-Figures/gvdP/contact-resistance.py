import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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
    'figure.figsize': (10/2.54, 6/2.54),  # 10x6 cm in inches (1 figure per line)
    # 'figure.figsize': (8/2.54, 6/2.54),  # 10x6 cm in inches (2 figures per line)
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

data1 = np.loadtxt("./Data-gvdP/20260509001.dat")
data2 = np.loadtxt("./Data-gvdP/20260509002.dat")
data3 = np.loadtxt("./Data-gvdP/20260509003.dat")

dataset =[
    data1, "-100", 3.11, -10.16, 'red', 'o',
    data2, "-200", 3.11, -10.31, 'blue', 's',
    data3, "-300", 3.10, -10.11, 'green', '^',
]

e = 1.60217662e-19
C = 2e-9
A = 32e-6
Ci = C / A
markevery = 4




# for data, label, mu, V_T, color, marker in zip(dataset[::6], dataset[1::6], dataset[2::6], dataset[3::6], dataset[4::6], dataset[5::6]):
#     V_G4 = data[:, 0]
#     I_34 = data[:, 2]
#     V_34 = data[:, 3]
#     V_14 = data[:, 4]
#     V_24 = data[:, 5]
#     V_12 = data[:, 6]
#     R_34 = V_34 / I_34
#     V_T = -10.2
#     V_del = -(V_G4 - V_T)

#     plt.plot(-V_G4, R_34*1e-6, color=color, label=label, marker=marker, markevery=markevery)


# plt.xlabel(r"Gate Voltage $-V_{G4}$ (V)")
# plt.ylabel(r"Total Resistance $R_{34}$ (M$\Omega$)")
# plt.xlim(15, 30)
# plt.ylim(0,100)
# plt.title(r"Total Resistance $R_{34}$ vs Gate Voltage $V_{G4}$")
# plt.legend(title=r"$I_{34}$ (nA)")
# plt.savefig("resistance.png", dpi=300)
# plt.savefig("resistance.pdf", dpi=300)
# plt.savefig("resistance.eps")
# plt.show()

V_G4 = data1[:, 0]
I_34 = data1[:, 2]
V_34 = data1[:, 3]
V_14 = data1[:, 4]
V_24 = data1[:, 5]
V_12 = data1[:, 6]
V_C = 0.5*(V_14 + V_24)
R_34 = V_34 / I_34
V_T = -10.2
V_del = -(V_G4 - V_C)

def func(x, a, b):
    return a + b/(x + V_T)

mask = (V_del > 15) & (V_del < 100)


popt, pcov = curve_fit(func, V_del[mask], R_34[mask])
R_34_fit = func(V_del[mask], *popt)
a = popt[0]
b = popt[1]

# 1-sigma parameter uncertainties from covariance matrix
perr = np.sqrt(np.diag(pcov))
a_err = perr[0]
b_err = perr[1]
r2 = 1 - np.sum((R_34[mask] - R_34_fit)**2) / np.sum((R_34[mask] - np.mean(R_34[mask]))**2)


print(rf"Background Resistance: ({a*1e-6:.2f} ± {a_err*1e-6:.2f}) MΩ")
print(rf"R^2: {r2:.4f}")


for data, label, mu, V_T, color, marker in zip(dataset[::6], dataset[1::6], dataset[2::6], dataset[3::6], dataset[4::6], dataset[5::6]):
    V_G4 = data[:, 0]
    I_34 = data[:, 2]
    V_34 = data[:, 3]
    V_14 = data[:, 4]
    V_24 = data[:, 5]
    V_12 = data[:, 6]
    R_34 = V_34 / I_34
    V_T = -10.2
    V_del = -(V_G4 - V_C)

    plt.plot(V_del, R_34*1e-6, color=color, label=label, marker=marker, markevery=markevery)

plt.plot(V_del[mask], R_34_fit*1e-6, color='red', linestyle='--', label=f"Fit {label}")
plt.xlabel(r"Effective Gate Voltage $-(V_{G4} - V_{C})$ (V)")
plt.ylabel(r"Total Resistance $R_{34}$ (M$\Omega$)")
plt.xlim(15, 30)
plt.ylim(0,100)
plt.title(r"Total Resistance $R_{34}$ vs Effective Gate Voltage $-(V_{G4} - V_{C})$")
plt.legend(title=r"$I_{34}$ (nA)")
plt.show()