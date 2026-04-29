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

data1 = np.loadtxt("./Data_20262904/20262904005.dat")
data2 = np.loadtxt("./Data_20262904/20262904005.snp")

R1 = 1e6
R2 = 1e5  # Resistance in ohms
Amp = -20

t = data2[:, 0]
V_charge = data2[:, 1]
V_discharge = data2[:, 2]
V_diff = V_charge + V_discharge 

# Define the fitting function: VR(t) = V_inf + Af*exp(-t/tau1) + As*exp(-(t/tau2)^beta)
def voltage_model(t, V_inf, Af, tau1, As, tau2, beta):
    return V_inf + Af * np.exp(-t / tau1) + As * np.exp(-(t / tau2) ** beta)

# Fit the charge curve
try:
    popt_charge, _ = curve_fit(voltage_model, t, V_charge, p0=[0, 1, 0.01, -1, 0.01, 1], maxfev=10000)
    V_charge_fit = voltage_model(t, *popt_charge)
    print("Charge curve fit parameters:")
    print(f"  V∞ = {popt_charge[0]:.6f} V")
    print(f"  Af = {popt_charge[1]:.6f} V")
    print(f"  τ1 = {popt_charge[2]:.6e} s")
    print(f"  As = {popt_charge[3]:.6f} V")
    print(f"  τ2 = {popt_charge[4]:.6e} s")
    print(f"  β = {popt_charge[5]:.6f}")
except Exception as e:
    print(f"Charge fit failed: {e}")
    V_charge_fit = None

# Fit the discharge curve
try:
    popt_discharge, _ = curve_fit(voltage_model, t, V_discharge, p0=[0, 1, 0.01, -1, 0.01, 1], maxfev=10000)
    V_discharge_fit = voltage_model(t, *popt_discharge)
    print("\nDischarge curve fit parameters:")
    print(f"  V∞ = {popt_discharge[0]:.6f} V")
    print(f"  Af = {popt_discharge[1]:.6f} V")
    print(f"  τ1 = {popt_discharge[2]:.6e} s")
    print(f"  As = {popt_discharge[3]:.6f} V")
    print(f"  τ2 = {popt_discharge[4]:.6e} s")
    print(f"  β = {popt_discharge[5]:.6f}")
except Exception as e:
    print(f"Discharge fit failed: {e}")
    V_discharge_fit = None

plt.figure(figsize=(10, 6))
plt.plot(t*1e3, V_charge, label='Charge (data)', color='blue', ls='-', lw=1.5, marker='o', markersize=4, markevery=100, alpha=0.7)
plt.plot(t*1e3, V_discharge, label='Discharge (data)', color='red', ls='-', lw=1.5, marker='^', markersize=4, markevery=100, alpha=0.7)

if V_charge_fit is not None:
    plt.plot(t*1e3, V_charge_fit, label='Charge (fit)', color='blue', ls='--', lw=2)
if V_discharge_fit is not None:
    plt.plot(t*1e3, V_discharge_fit, label='Discharge (fit)', color='red', ls='--', lw=2)

plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.title('DLTS Signal vs Time with Fitted Curves')
plt.xlim(0.00, 50)
plt.ylim(0, 3)
plt.legend(frameon=True, numpoints=1)
plt.grid(True, alpha=0.3)
plt.show()

# plt.plot(t*1e3, V_diff, label='Difference', color='green', ls='-', lw = 1.5, marker='s', markersize=4, markevery=100)
# plt.xlabel('Time (ms)')
# plt.ylabel('Voltage (V)')
# plt.title('Difference vs Time')
# plt.show()

