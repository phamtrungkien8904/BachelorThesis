import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Custom settings
plt.style.use('classic')
plt.rcParams.update({
    'figure.dpi': 100,
    'figure.figsize': (10, 6),
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


C = 2.1e-9
n2D = 1.99e12 * 1e4
e = 1.602e-19
m = 0.26 * 9.109e-31
epsilon = 11.7 
Z0 = 376.73
Ref = 2*np.sqrt(epsilon)/Z0

data = np.loadtxt('20260526_FreqDomain.dat')
f = data[:, 0]
Re = data[:, 1]* Ref
Im = data[:, 2]* Ref
f *= 1e12


def func_1(x, a):
    return a 

popt_1, pcov_1 = curve_fit(func_1, f, Re)
Re_fit = func_1(f, *popt_1)
a = float(popt_1[0])
f_fit = np.linspace(0, f.max(), 500)


# 1-sigma parameter uncertainties from covariance matrix
perr_1 = np.sqrt(np.diag(pcov_1))
a_err = float(perr_1[0])

def func_2(x, b):
    return a**2 *m/(n2D* e**2) * 2*np.pi*x + b

popt_2, pcov_2 = curve_fit(func_2, f, Im)
Im_fit = func_2(f, *popt_2)
b = float(popt_2[0])


# 1-sigma parameter uncertainties from covariance matrix
perr_2 = np.sqrt(np.diag(pcov_2))
b_err = float(perr_2[0])

plt.plot(f, Re, 'o-', label='Re')
plt.plot(f, Im, 's-', label='Im')
plt.axhline(y=a, color='r', linestyle='--')

plt.plot(f_fit, func_2(f_fit, *popt_2), color='b', linestyle='--')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Conductivity (S)')
plt.title('Frequency-Dependent Conductivity')
plt.legend()
plt.show()

tau = a*m/(n2D*e**2) *1e15
tau_err = a_err*m/(n2D*e**2) *1e15
null = -b/(a**2 *m/(n2D* e**2) * 2*np.pi) *1e-12
print(f"Relaxation time (tau): ({tau:.2f}  ± {tau_err:.2f}) fs")
print(f"Null frequency: {null:.2f} THz")