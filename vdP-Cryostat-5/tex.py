import shutil
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

# # 1. Clear out Matplotlib's old compiler paths and text layouts from disk
# cache_dir = mpl.get_cachedir()
# if os.path.exists(cache_dir):
#     shutil.rmtree(cache_dir)

# # 2. Hard-override the Windows environment PATH variables *inside* Python
# # This pushes your new User installation to the absolute front of the priority line
# user_bin = r"C:\Users\Kien.Pham\AppData\Local\Programs\MiKTeX-user\miktex\bin\x64"
# os.environ["PATH"] = user_bin + os.path.pathsep + os.environ["PATH"]


# Custom settings
plt.style.use('classic')

plt.rcParams.update({
    "text.usetex": True,
    # 'text.latex.preamble': r'''
    # \usepackage[T1]{fontenc}
    # \usepackage{lmodern}
    # \usepackage[utf8]{inputenc}
    # \usepackage{amsmath},
    # \usepackage{amssymb}
    # \usepackage{siunitx},
    # '''
})
plt.rcParams.update({
    # Figure settings
    'figure.dpi': 100,
    'figure.figsize': (10, 6),
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.linewidth': 2,
    'axes.labelsize': 18,
    'axes.titlesize': 20,
    'axes.labelcolor': 'black',
    'savefig.facecolor': 'white',
    'font.family': 'sans-serif',
    'font.sans-serif': 'Arial',
    'mathtext.fontset': 'cm',
    'figure.constrained_layout.use': True,

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
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,  

    # Legend
    # 'legend.frameon': False,
    # 'legend.fontsize': 18,
    # 'legend.loc': 'best',
    # 'legend.numpoints': 1,
})

# data = np.loadtxt("./Data-Mani/01.dat")
data = np.loadtxt("./Data-Mani/09.dat")
data = np.loadtxt("./gvdP/20260512005.dat")

V_GS = data[:, 0]
I_DS = data[:, 2]
V_DS = data[:, 3]
V_C = 0.5 * (data[:, 4] + data[:, 5])
V_12 = data[:, 6]
sigma = -data[:, 7]
V_del = -(V_GS - V_C)

# plt.plot(
#     V_del,
#     sigma * 1e6,
#     color='red',
#     marker='o',
#     markevery=1,
#     ls='-',
#     markeredgecolor="white", markeredgewidth=1, markersize=7
#     )

# plt.xlabel(r"$V_{GS} - V_C$ (V)")
# plt.ylabel(r"$\sigma$ ($\mu$S/sq.)")
# plt.title("Conductivity vs. Gate Voltage")
# plt.show()

C = 1.8e-9
A = 32e-6
Ci = C / A

def func(x, a, b):
    return a*x + b

mask = (V_del > 20) & (V_del < 40)


popt, pcov = curve_fit(func, V_del[mask], sigma[mask])
sigma_fit = func(V_del, *popt)
a = popt[0]
b = popt[1]

mu = a / Ci * 1e4
V_T = -b / a

print(rf"Mobility ($\mu$): {mu:.2f} cm^2/Vs")
print(rf"Threshold Voltage ($V_T$): {V_T:.2f} V")



# 1-sigma parameter uncertainties from covariance matrix
perr = np.sqrt(np.diag(pcov))

plt.plot(
    V_del,
    sigma * 1e6,
    color='red',
    marker='o',
    markevery=1,
    ls='-',
    label='Data',
    markeredgecolor="white", markeredgewidth=1, markersize=7
    )
plt.plot(
    V_del,
    sigma_fit * 1e6,
    color='blue',
    ls='-',
    label=f'Fit'
    )
plt.xlabel(r"Gate Voltage $V_{G4}$ (V)")
plt.ylabel(r"Conductance $\sigma$ ($\mu$S/sq.)")
plt.title("Conductivity vs. Gate Voltage with Fit (260K)")
# plt.xlim(0,50)
# plt.ylim(0, 0.0001)  # Convert to μS/sq. for y-axis limits
plt.legend()
# plt.savefig("sigma_cold.eps", format = 'eps')
plt.show()




