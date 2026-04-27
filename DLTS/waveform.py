import numpy as np
import matplotlib.pyplot as plt

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

data = np.loadtxt("./Data/20262704003.dat")

R = 100e3  # Resistance in ohms

t = data[:, 0]
V_R = data[:, 1]
main_trigger = data[:, 2]
V_in = data[:, 3]
second_trigger = data[:, 4]
I = data[:, 5]
V_C = V_in - V_R

plt.plot(t, V_in, label='V_in')
# plt.plot(t, V_R, label='V_R')
plt.plot(t, V_C, label='V_C')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Input and Output Voltage vs Time')
plt.legend()
plt.show()
