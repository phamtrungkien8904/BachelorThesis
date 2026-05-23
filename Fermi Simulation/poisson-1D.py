import numpy as np
import matplotlib.pyplot as plt
import time

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

start_time = time.time()
N = 101
iter = 50000000 # Kerting's original code uses 1000 iterations, but you can increase this for better convergence at the cost of longer runtime. (Best: 2000000)
step_iter = iter//10
L = 5e-3  # Physical size of the domain in meters
x = np.linspace(0, L, N)
dx = x[1] - x[0]


k_B = 1.380649e-23  # Boltzmann constant in J/K
T = 300
e = 1.602176634e-19  # Elementary charge in Coulombs
V_T = k_B * T / e
print(f"Thermal voltage (V_T): {V_T:.4f} V")
n_i = 1.5e10 # Intrinsic carrier concentration in m^-3 (Si)



epsilon = 3 * 8.854187817e-12  # Permittivity of semiconductor (epsilon_r * epsilon_0) in F/m
N_D = np.zeros(N)
C_D = 1e15  # Donator concentration in m^-3
N_D[N//2:N] = C_D  # Donator concentration in m^-3
N_A = np.zeros(N)
C_A = 3e15  # Acceptor concentration in m^-3
N_A[:N//2] = C_A  # Acceptor concentration in m^-3

V_ext = -1.0  # External voltage in volts
V_bi = V_T * np.log(C_A * C_D / n_i**2)  # Built-in potential in volts
print(f"Calculated built-in potential (V_bi): {V_bi:.4f} V")
d_n = np.sqrt(2 * epsilon * (V_bi - V_ext) / e *C_A/C_D * 1/(C_A + C_D))  # Depletion width in meters
d_p = np.sqrt(2 * epsilon * (V_bi - V_ext) / e *C_D/C_A * 1/(C_A + C_D))  # Depletion width in meters
W = d_n + d_p  # Total depletion width in meters
print(f"Depletion width (W): {W*1e9:.2f} nm")

V = np.zeros(N)
p = np.zeros(N)  # Hole concentration (m^-3)
n = np.zeros(N)  # Electron concentration (m^-3)

contact_mask = np.zeros(N, dtype=bool)

d_n_cells = max(1, int(round(d_n / dx)))
d_p_cells = max(1, int(round(d_p / dx)))

p[:N//2 - d_p_cells] = N_A[0]  # Hole concentration in the acceptor region
n[N//2 + d_n_cells:] = N_D[N-1]  # Electron concentration in the donor region
rho = e*(p - n + N_D - N_A)  # Net charge density (C/m^3)

contact_size = 0.1
contact_width = int(contact_size * N)
V[:contact_width] = V_bi
# V[-contact_width:] = 0.0
contact_mask[:contact_width] = True
# contact_mask[-contact_width:] = True



def solve():
    global V, rho

    contact_V = V.copy()
    alpha = 0.05
    error = np.zeros(iter)

    for i in range(iter):
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
stop_time = time.time()
print(f"Runtime: {stop_time - start_time:.2f} seconds.")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

ax1.plot(x * 1e9, V, color='blue')
ax1.set_ylabel('Potential (V)')
ax1.set_title('1D Poisson Equation Solution')
# ax1.set_xlim(0, L * 1e9)
# ax1.set_ylim(-np.max(V) * 1.5, np.max(V) * 1.5)

ax2.plot(x * 1e9, rho, color='red')
ax2.set_xlabel('Position (nm)')
ax2.set_ylabel('Net Charge Density (C/m^3)')
# ax2.set_xlim(0, L * 1e9)
# ax2.set_ylim(-np.max(rho) * 1.5, np.max(rho) * 1.5)
fig.tight_layout()
plt.show()
