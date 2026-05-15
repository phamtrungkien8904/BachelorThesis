import numpy as np  
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

data1_dens = np.loadtxt('Proj031Dens.dat')
data1_poti = np.loadtxt('Proj031Poti.dat')
data1_n2D = np.loadtxt('Proj031n2D.dat')

data2_dens = np.loadtxt('Proj032Dens.dat')
data2_poti = np.loadtxt('Proj032Poti.dat')
data2_n2D = np.loadtxt('Proj032n2D.dat')

data3_dens = np.loadtxt('Proj033Dens.dat')
data3_poti = np.loadtxt('Proj033Poti.dat')
data3_n2D = np.loadtxt('Proj033n2D.dat')

x = np.linspace(0, 50, 51)

rho_1 = data1_dens[0,:]
V_1 = data1_poti[0,:]
n2D_1 = data1_n2D[0,:]

rho_2 = data2_dens[0,:]
V_2 = data2_poti[0,:]
n2D_2 = data2_n2D[0,:]

rho_3 = data3_dens[0,:]
V_3 = data3_poti[0,:]
n2D_3 = data3_n2D[0,:]

# Linear fit function
def func(x, a, b):
    return a * x + b

mask = (V_1 > -0.37) & (V_1 < -0.1)
popt_1, pcov_1 = curve_fit(func, V_1[mask], np.log(n2D_1[mask]))
popt_2, pcov_2 = curve_fit(func, V_1[mask], np.log(rho_1[mask]))

a1, b1 = popt_1
a2, b2 = popt_2

perr_1 = np.sqrt(np.diag(pcov_1))
perr_2 = np.sqrt(np.diag(pcov_2))

fit_1 = func(V_1, *popt_1)
fit_2 = func(V_1, *popt_2)

print(f"rho: a = {a1:.4f} ± {perr_1[0]:.4f}, b = {b1:.4f} ± {perr_1[1]:.4f}")
print(f"n2D: a = {a2:.4f} ± {perr_2[0]:.4f}, b = {b2:.4f} ± {perr_2[1]:.4f}")
print(f"Thermal Voltage (rho): V_th = {-1/a1:.4f} V")
print(f"Thermal Voltage (n2D): V_th = {-1/a2:.4f} V")

print(np.exp(b2 - b1))


plt.plot(V_1, np.log(n2D_1), '^', label='rho')
plt.plot(V_1, np.log(rho_1), 'o', label='n2D')
plt.plot(V_1, fit_1, 'r--', label='Fit rho')
plt.plot(V_1, fit_2, 'g--', label='Fit n2D')
# plt.semilogy(V_1, rho_1 - n2D_1, 's', label='Project 3')
plt.xlabel('Potential (V)')
plt.ylabel('Density ()')
plt.legend()
plt.axhline(0, color='black', lw=0.5, ls='--')
plt.show()

fig = plt.figure(figsize=(10, 8))
ratio = 1.0
fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
image = plt.imshow(data1_dens, extent=[0, 50, 0, 50], origin='lower', aspect='auto')
plt.colorbar(image, label='Density')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Density Distribution for Project 1')
plt.show()

