import numpy as np
import matplotlib.pyplot as plt
import time

# Custom settings
plt.style.use('classic')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['figure.dpi'] = 100

start_time = time.time()

# Simulation parameters
N = 101
iter = 100000 # Kerting's original code uses 1000 iterations, but you can increase this for better convergence at the cost of longer runtime. (Best: 2000000)
step_iter = iter//10
L = 50e-6  # Physical size of the domain in meters
x = np.linspace(0, L, N)
dx = x[1] - x[0]

# Physical constants
k_B = 1.380649e-23  # Boltzmann constant in J/K
T = 300
e = 1.602176634e-19  # Elementary charge in Coulombs
epsilon = 3 * 8.854187817e-12  # Permittivity of semiconductor (epsilon_r * epsilon_0) in F/m

V_T = k_B * T / e
print(f"Thermal voltage (V_T): {V_T:.4f} V")
V_bi = V_T * 4  # Built-in potential in volts
V_ext = 0.05  # External voltage in volts
V_tot = V_bi - V_ext  # Effective built-in potential in volts
print(f"Calculated built-in potential (V_bi): {V_bi:.4f} V")
print(f"Total potential (V_tot): {V_tot:.4f} V")
N_A = 1e18  # Acceptor concentration in m^-3
p_edge = N_A * np.exp(V_tot / V_T)  # Hole concentration at the edge of the accumulation region in m^-3

V = np.zeros(N)
p = np.zeros(N)  # Hole concentration (m^-3)
rho = np.zeros(N)  # Net charge density (C/m^3)

contact_mask = np.zeros(N, dtype=bool)

contact_size = 0.1
contact_width = int(contact_size * N) + 1
V[:contact_width] = 0.0
# V[-contact_width:] = 0.0
contact_mask[:contact_width] = True
# contact_mask[-contact_width:] = True

# Accumulation width estimation for initial guess
W = np.sqrt(2 * epsilon * V_tot / (e * N_A))  # Accumulation width in meters
print(f"Estimated accumulation width (W): {W*1e6:.2f} um")
def solve():
    global V, rho, p

    contact_V = V.copy()
    alpha = 0.05
    error = np.zeros(iter)

    for i in range(iter):
        p = N_A * np.exp((-V + V_tot) / V_T)  # Hole concentration using Boltzmann approximation
        p[contact_mask] = p_edge 
        rho = e * (p - N_A)  # Net charge density (C/m^3)
        rho[contact_mask] = 0  # Net charge density at the contact (C/m^3)

        V_new = V.copy()
        V_new[1:-1] = 0.5 * (V[:-2] + V[2:] + dx**2 * rho[1:-1] / epsilon)

        # Neumann outer boundaries: dV/dn = 0
        V_new[0] = V_new[1]
        V_new[-1] = V_new[-2]

        # Dirichlet contacts
        V_new[contact_mask] = contact_V[contact_mask]

        # Relaxation
        error[i] = 100.0 * np.max(np.abs(V_new - V)) / max(np.max(np.abs(V)), 1e-30)
        V = (1 - alpha) * V + alpha * V_new

        if (i + 1) % step_iter == 0:
            print(f"Iteration: {i + 1}/{iter}, Error: {error[i]:.6e} %")

    return V, rho, error

V, rho, error = solve()
np.savetxt("./Data-Export/ohmic_Poti.dat", V)
np.savetxt("./Data-Export/ohmic_pDens.dat", p)

stop_time = time.time()
print(f"Runtime: {stop_time - start_time:.2f} seconds.")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

ax1.plot(x * 1e6, V, color='blue', lw=2)
ax1.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='--')
ax1.set_ylabel('Potential (V)')
ax1.set_title('Ohmic Barrier (p-type) Simulation', fontsize=18)
ax1.set_xlim(0, L * 1e6)
ax1.set_ylim(-np.max(V) * 1.5, np.max(V) * 1.5)

ax2.plot(x * 1e6, p, color='red', lw=2)
ax2.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='--')
ax2.set_xlabel('Position (um)')
ax2.set_ylabel('Hole Concentration (m^-3)')
ax2.set_xlim(0, L * 1e6)
ax2.set_ylim(0, np.max(p) * 1.5)
fig.tight_layout()
plt.show()

