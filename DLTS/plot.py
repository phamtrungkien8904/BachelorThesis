import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Custom settings
plt.style.use('classic')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['figure.dpi'] = 100

log = np.loadtxt("Log.csv", delimiter=",", skiprows=1)
V = log[:, 0]
a1 = log[:, 1]
b1 = log[:, 2]
c1 = log[:, 3]
a2 = log[:, 4]
b2 = log[:, 5]
c2 = log[:, 6]
x_intersec = log[:, 7]

plt.plot(V, c1, marker='o', linestyle='-', color='blue')
plt.show()