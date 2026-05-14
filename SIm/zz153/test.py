import numpy as np  
import matplotlib.pyplot as plt

data1_dens = np.loadtxt('Proj021Dens.dat')
data1_poti = np.loadtxt('Proj021Poti.dat')
data2_dens = np.loadtxt('Proj022Dens.dat')
data2_poti = np.loadtxt('Proj022Poti.dat')
data3_dens = np.loadtxt('Proj023Dens.dat')
data3_poti = np.loadtxt('Proj023Poti.dat')

x = np.linspace(0, 50, 51)
rho_1 = data1_dens[0,:]
V_1 = data1_poti[0,:]
rho_2 = data2_dens[0,:]
V_2 = data2_poti[0,:]
rho_3 = data3_dens[0,:]
V_3 = data3_poti[0,:]


plt.plot(V_1, rho_1, '^', label='Project 1')
plt.plot(V_2, rho_2, 'o', label='Project 2')
plt.plot(V_3, rho_3, 's', label='Project 3')
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
