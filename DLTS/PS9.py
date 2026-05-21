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

data1 = np.loadtxt("./Data_20262904/20262904005.snp") # 40V
data2 = np.loadtxt("./Data_20262904/20262904004.snp") # 35V
data3 = np.loadtxt("./Data_20262904/20262904001.snp") # 30V
data4 = np.loadtxt("./Data_20262904/20262904002.snp") # 25V
data5 = np.loadtxt("./Data_20262904/20262904003.snp") # 20V
data6 = np.loadtxt("./Data_20262904/20262904006.snp") # 15V
data7 = np.loadtxt("./Data_20262904/20262904007.snp") # 10V

dataset = [
    ("-40 V", -40, data1, 'red'),
    ("-35 V", -35, data2, 'orange'),
    ("-30 V", -30, data3, 'green'),
    ("-25 V", -25, data4, 'blue'),
    # ("-20 V", -20, data5, 'purple'),
    # ("-15 V", -15, data6, 'brown'),
    # ("-10 V", -10, data7, 'cyan')
]


R1 = 1e6  # 1 MΩ
R2 = 1e5 # 1 MΩ
# plt.figure(figsize=(8, 8))
# # plt.plot(t*1e3, I_discharge*1e6, label='Discharge Current', color='red', ls='-', lw = 1.5)
# # plt.plot(t*1e3, I_charge*1e6, label='Charge Current', color='blue', ls='-', lw = 1.5)
# for label, voltage, data, color in dataset:
#     t = data[:, 0]
#     V_discharge = data[:, 2]
#     I_discharge = V_discharge/R2
#     V_charge = data[:, 1]
#     I_charge = V_charge/R2
#     plt.plot(t*1e3, -I_charge*1e6, label=label, color=color, ls='-', lw=1.5)

# plt.axhline(y=0.0, color='black', ls='--', lw=1)
# plt.xlabel('Time (ms)', fontsize=19)
# plt.ylabel(r'Current ($\mu$A)', fontsize=19)
# plt.title('DLTS Signal vs Time', fontsize=20)
# plt.xlim(0, 50)
# plt.ylim(0, 20)
# plt.legend(frameon=True, numpoints=1, fontsize=15)
# # plt.savefig('DLTS_pulse-var.eps', format='eps', bbox_inches='tight')
# plt.show()


# plt.figure(figsize=(8, 6))
# # plt.plot(t*1e3, I_discharge*1e6, label='Discharge Current', color='red', ls='-', lw = 1.5)
# # plt.plot(t*1e3, I_charge*1e6, label='Charge Current', color='blue', ls='-', lw = 1.5)
# for label, voltage, data, color in dataset:
#     t = data[:, 0]
#     V_discharge = data[:, 2]
#     I_discharge = V_discharge/R2
#     V_charge = data[:, 1]
#     I_charge = V_charge/R2
#     plt.plot(t*1e3, -(voltage - I_charge*(R1 + R2)), label=label, color=color, ls='-', lw=1.5)
#     plt.axhline(y=-voltage, color='black', ls='--', lw=1)

# plt.axhline(y=0.0, color='black', ls='--', lw=1)
# plt.xlabel('Time (ms)', fontsize=19)
# plt.ylabel(r'Voltage (V)', fontsize=19)
# plt.title('DLTS Signal vs Time', fontsize=20)
# plt.xlim(0, 50)
# # plt.ylim(-2, 2)
# plt.legend(frameon=True, numpoints=1, fontsize=15)
# plt.show()




t = data1[:, 0]
V_discharge = data1[:, 2]
V_charge = data1[:, 1]
I_discharge = V_discharge/R2
I_charge = -V_charge/R2

plt.figure(figsize=(8, 6))
plt.plot(t*1e3, I_charge*1e6, label='Charge Current', color='red', ls='-', lw=1.5)
plt.axhline(y=0.0, color='black', ls='--', lw=1)
plt.xlabel('Time (ms)', fontsize=19)
plt.ylabel(r'Current ($\mu$A)', fontsize=19)
plt.title('DLTS Signal vs Time', fontsize=20)
plt.xlim(0, 90)
# plt.ylim(-2, 2)
plt.legend(frameon=True, numpoints=1, fontsize=15)
# plt.savefig('DLTS_current.eps', format='eps', bbox_inches='tight')
plt.show()


def func(x, a1, b1, c1):
    return a1 * np.exp(-x / b1) + c1


mask = (t >= 0.0000) & (t <= 0.01)
# Initial guesses: a ~ peak current in window, b ~ C_actual*(R1+R2) (time constant)
if np.any(mask):
    a1_0 = np.max(I_charge[mask]) - np.min(I_charge[mask])
C_actual = 0.2e-9  # 10 nF
b1_0 = C_actual * (R1 + R2)
c1_0 = np.min(I_charge[mask])
p1_0 = [a1_0, b1_0, c1_0]

popt1, pcov1 = curve_fit(func, t[mask], I_charge[mask], p0=p1_0, maxfev=10000)
sigma_fit1 = func(t[mask], *popt1)
a1, b1, c1 = popt1

# Coefficient of determination
ss_res = np.sum((I_charge[mask] - sigma_fit1) ** 2)
ss_tot = np.sum((I_charge[mask] - np.mean(I_charge[mask])) ** 2)
r2 = 1 - (ss_res / ss_tot)

# 1-sigma parameter uncertainties from covariance matrix
perr = np.sqrt(np.diag(pcov1))
a1_err, b1_err, c1_err = perr

R_L = a1/c1*(R1 + R2)
R_L_err = R_L * np.sqrt((a1_err/a1)**2 + (c1_err/c1)**2)
C1 = b1 / (1/(R1 + R2) + 1/R_L)**(-1)
C1_err = b1_err / (1/(R1 + R2) + 1/R_L)**(-1)

print(f"a = {a1:.3g} ± {a1_err:.3g}")
print(f"b = {b1:.3g} ± {b1_err:.3g}")
print(f"c = {c1:.3g} ± {c1_err:.3g}")
print(f"R^2 = {r2:.3f}")
print("-----------------------------")
print(f"C1 (fitted) = ({C1*1e9:.3f} ± {C1_err*1e9:.3f}) nF")
print(f"R_L (fitted) = ({R_L/1e6:.3f} ± {R_L_err/1e6:.3f}) MΩ")

V_T = 5
I_L = (30 - V_T) / R_L
print(f"Leakage current I_L = {I_L*1e9:.3f} nA")


x1 = np.linspace(0.00, 0.02, 100)
plt.figure(figsize=(8, 8))
plt.plot(t*1e3, I_charge*1e6, '^', label='Data', color='red', markersize=6, ls='-', lw = 1.5, markevery=20)
plt.plot(x1*1e3, func(x1, *popt1)*1e6, lw=2, label=rf'Fit: $C={C1*1e9:.3f}$ nF', color='blue', linestyle='--')
plt.xlabel(r"Time (ms)")
plt.ylabel(r"Current signal (uA)")
plt.xlim(0.00, 10)
# plt.ylim(-0.01, 1.5)
plt.legend(frameon=True, loc='upper right', numpoints=1, fontsize=12)
plt.title("Discharge of a Capacitor through a Resistor", fontsize=14)
plt.savefig("DLTS-first.eps", format='eps', bbox_inches='tight')
plt.show()


plt.figure(figsize=(8, 6))
plt.plot(t*1e3, I_charge*1e6, label='Charge Current', color='red', ls='-', lw=1.5)
plt.axhline(y=0.0, color='black', ls='--', lw=1)
plt.xlabel('Time (ms)', fontsize=19)
plt.ylabel(r'Current ($\mu$A)', fontsize=19)
plt.title('DLTS Signal vs Time', fontsize=20)
plt.xlim(10, 90)
# plt.ylim(-2, 2)
plt.legend(frameon=True, numpoints=1, fontsize=15)
# plt.savefig('DLTS_current.eps', format='eps', bbox_inches='tight')
plt.show()


def func(x, a2, b2, c2):
    return a2 * np.exp(-x / b2) + c2


mask = (t >= 0.02) & (t <= 0.09)
# Initial guesses: a ~ peak current in window, b ~ C_actual*(R1+R2) (time constant)
if np.any(mask):
    a2_0 = np.max(I_charge[mask]) - np.min(I_charge[mask])
C_actual = 10e-9  # 10 nF
b2_0 = C_actual * (R1 + R2)
c2_0 = np.min(I_charge[mask])
p2_0 = [a2_0, b2_0, c2_0]

popt2, pcov2 = curve_fit(func, t[mask], I_charge[mask], p0=p2_0, maxfev=10000)
sigma_fit2 = func(t[mask], *popt2)
a2, b2, c2 = popt2

# Coefficient of determination
ss_res = np.sum((I_charge[mask] - sigma_fit2) ** 2)
ss_tot = np.sum((I_charge[mask] - np.mean(I_charge[mask])) ** 2)
r2 = 1 - (ss_res / ss_tot)

# 1-sigma parameter uncertainties from covariance matrix
perr = np.sqrt(np.diag(pcov2))
a2_err, b2_err, c2_err = perr

R_L = a2/c2*(R1 + R2)
R_L_err = R_L * np.sqrt((a2_err/a2)**2 + (c2_err/c2)**2)
C2 = b2 / (1/(R1 + R2) + 1/R_L)**(-1)
C2_err = b2_err / (1/(R1 + R2) + 1/R_L)**(-1)

print(f"a = {a2:.3g} ± {a2_err:.3g}")
print(f"b = {b2:.3g} ± {b2_err:.3g}")
print(f"c = {c2:.3g} ± {c2_err:.3g}")
print(f"R^2 = {r2:.3f}")
print("-----------------------------")
print(f"C2 (fitted) = ({C2*1e9:.3f} ± {C2_err*1e9:.3f}) nF")
print(f"R_L (fitted) = ({R_L/1e6:.3f} ± {R_L_err/1e6:.3f}) MΩ")

V_T = 5
I_L = (30 - V_T) / R_L
print(f"Leakage current I_L = {I_L*1e9:.3f} nA")


x2 = np.linspace(0.01, 0.09, 100)
plt.figure(figsize=(8, 8))
plt.plot(t*1e3, I_charge*1e6, '^', label='Data', color='red', markersize=6, ls='-', lw = 1.5, markevery=200)
plt.plot(x2*1e3, func(x2, *popt2)*1e6, lw=2, label=rf'Fit: $C={C2*1e9:.3f}$ nF', color='blue', linestyle='--')
plt.xlabel(r"Time (ms)")
plt.ylabel(r"Current signal (uA)")
plt.xlim(10, 90)
plt.ylim(0, 5)
plt.legend(frameon=True, loc='upper right', numpoints=1, fontsize=12)
plt.title("Discharge of a Capacitor through a Resistor", fontsize=14)
plt.savefig("DLTS-second.eps", format='eps', bbox_inches='tight')
plt.show()

# x_intersec = -b2*np.log((c1 - c2)/a2)
# x1 = np.linspace(0.00, x_intersec, 100)
# x2 = np.linspace(x_intersec, 0.09, 100)
# plt.figure(figsize=(8, 8))
# plt.plot(t*1e3, I_charge*1e6, label='Charge Current', color='red', ls='-', lw=1.5)
# plt.plot(x1*1e3, func(x1, *popt1)*1e6, label=rf'Fit: $C={C1*1e9:.3f}$ nF', color='blue', ls='--', lw=2)
# plt.plot(x2*1e3, func(x2, *popt2)*1e6, label=rf'Fit: $C={C2*1e9:.3f}$ nF', color='blue', ls='--', lw=2)
# plt.axhline(y=0.0, color='black', ls='--', lw=1)
# plt.xlabel('Time (ms)', fontsize=19)
# plt.ylabel(r'Current ($\mu$A)', fontsize=19)
# plt.title('DLTS Signal vs Time', fontsize=20)
# plt.xlim(0, 90)
# plt.ylim(0, 20)
# plt.legend(frameon=True, numpoints=1, fontsize=15)
# plt.savefig('DLTS_fullfit.eps', format='eps', bbox_inches='tight')
# plt.show()

# Save as a single row in the CSV
# np.savetxt("Log_10V.csv", np.array([-10,a1, b1, c1, a2, b2, c2, x_intersec]).reshape(1, -1), delimiter=",")