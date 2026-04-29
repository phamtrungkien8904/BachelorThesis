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

t = np.linspace(0, 0.05, 500)  # Time array from 0 to 50 ms
C1 = 3e-9  # Capacitance in farads
C2 = 6e-9  # Capacitance in farads
R = 1e6  # Resistance in ohms

def func(t):
    return 1*np.exp(-t/(R*C1)) + 0.1*np.exp(-(t/(R*C2))**0.5)

plt.plot(t*1e3, func(t), label='Theoretical Fit', color='blue', lw=2, linestyle='--')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage signal (V)')
plt.show() 