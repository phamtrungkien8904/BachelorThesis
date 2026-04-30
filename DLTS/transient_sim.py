# Transient Simulation of a First-Order System RC Circuit
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

# Parameters for the RC circuit
R = 1e6  # Resistance in ohms
C0 = 3e-9  # Capacitance in farads
# Time array from 0 to 50 ms
t = np.linspace(0, 0.05, 5000)
V0 = 1.0  # Step input voltage in volts
V_in = V0 * np.ones_like(t)

# Time varying capacitor value to simulate a non-linear response
CS = 1e-9  # Capacitance in farads
C = (1/C0 + np.exp(-t/0.0001)/CS)**(-1)

# Voltage response of the RC circuit to a step input
def solve():
    V_C = np.zeros_like(t)
    V_R = np.zeros_like(t)
    for i in range(1, len(t)):
        dt = t[i] - t[i-1]
        V_C[i] = V_C[i-1] + (V_in[i-1] - V_C[i-1]) / (R * C[i-1]) * dt
        V_R[i] = V_in[i-1] - V_C[i]
    return V_R

V_R = solve()
# Plotting the results

plt.plot(t*1e3, V_R, label='Voltage across the capacitor', color='red', lw=2)
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.title('Transient Response of an RC Circuit to a Step Input')
plt.grid()
plt.legend()
plt.show()

print(C)