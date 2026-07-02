import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Custom settings for python figures
plt.style.use('classic')

# plt.rcParams.update({
#     "text.usetex": True,
#     'text.latex.preamble': r'''
#     \usepackage[T1]{fontenc}
#     \usepackage{lmodern}
#     \usepackage[utf8]{inputenc}
#     \usepackage{amsmath}
#     \usepackage{amssymb}
#     \usepackage{siunitx}
#     \usepackage{sfmath}
#     '''
# })
plt.rcParams.update({
    # Figure settings
    'figure.dpi': 300,
    # 'figure.figsize': (10/2.54, 6/2.54),  # 10x6 cm in inches (1 figure per line)
    'figure.figsize': (8/2.54, 6/2.54),  # 10x6 cm in inches (2 figures per line)
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


C = 2.1e-9
# n2D = 1.99e12 * 1e4
e = 1.602e-19
m = 0.26 * 9.109e-31
epsilon = 11.7 
Z0 = 376.73
Ref = 2*np.sqrt(epsilon)/Z0

data = np.loadtxt('20260526001.dat')
f = data[:, 0]
Re = data[:, 1]* Ref
Im = data[:, 2]* Ref
f *= 1e12


def func_1(x, a):
    return a 

popt_1, pcov_1 = curve_fit(func_1, f, Re)
Re_fit = func_1(f, *popt_1)
a = float(popt_1[0])
f_fit = np.linspace(0, 3e12, 500)


# 1-sigma parameter uncertainties from covariance matrix
perr_1 = np.sqrt(np.diag(pcov_1))
a_err = float(perr_1[0])

def func_2(x, n2D):
    return a**2 *m/(n2D* e**2) * 2*np.pi*x 

mask = (f > 0.5e12) & (f < 3e12)
popt_2, pcov_2 = curve_fit(func_2, f[mask], Im[mask])
Im_fit = func_2(f[mask], *popt_2)
n2D = float(popt_2[0])


# 1-sigma parameter uncertainties from covariance matrix
perr_2 = np.sqrt(np.diag(pcov_2))
n2D_err = float(perr_2[0])


tau = a*m/(n2D*e**2) *1e15
tau_err = a_err*m/(n2D*e**2) *1e15
n2D = n2D * 1e-4

plt.scatter(f*1e-12, Re*1e6, color='r', label='Re data', marker='o')
plt.scatter(f*1e-12, Im*1e6, color='b', label='Im data', marker='s')
plt.axhline(y=a*1e6, color='r', linestyle='-', label=f'Re fit')
plt.axhline(y=0, color='k', linestyle='--')

plt.plot(f_fit*1e-12, func_2(f_fit, *popt_2)*1e6, color='b', linestyle='-', label=f'Im fit')
plt.xlabel('Frequency (THz)')
plt.ylabel(r'$\Delta S / S \times 10^6$')
plt.title(f'THz Electromodulation Spectroscopy\n$\\tau = {tau:.2f}$ fs, $n_{{2D}} = {n2D:.2e}$ cm$^{{-2}}$')
plt.xlim(0, 3)
plt.legend(numpoints=1)



print(f"Relaxation time (tau): ({tau:.2f}  ± {tau_err:.2f}) fs")
print(f"2D Carrier Density (n2D): ({n2D:.2e}  ± {n2D_err:.2e}) cm^-2")

plt.savefig('THz_fit.png', dpi=300)
plt.show()