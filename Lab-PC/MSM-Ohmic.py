import numpy as np
import matplotlib.pyplot as plt
import time
File_index = "01"
try:
    import msvcrt
except ImportError:
    msvcrt = None

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
N = 201
iter = 10000000 # Kerting's original code uses 1000 iterations, but you can increase this for better convergence at the cost of longer runtime. (Best: 2000000)
step_iter = 100
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
V_bi = V_T * 2  # Built-in potential in volts
V_G = 0  # External voltage in volts (Reverse: V_ext < 0, Forward: V_ext > 0)
V_tot = V_bi + V_G  # Effective built-in potential in volts
V_D = 0 # Drain Voltage

print(f"Built-in potential (V_bi): {V_bi:.4f} V")
print(f"Total potential (V_tot): {V_tot:.4f} V")
print(f"Drain voltage (V_D): {V_D:.4f} V")
N_A = 1e18  # Acceptor concentration in m^-3
N_v = 1e19  # Effective density of states in the valence band in m^-3
p_edge = N_A * np.exp(V_bi / V_T)  # Hole concentration at the edge of the depletion region in m^-3
E_B = e*V_T*(np.log(N_v/N_A) - V_bi/V_T)  # Barrier energy in Joules
print(f"Barrier energy (E_B): {E_B/e:.4f} eV")

V = np.zeros(N)
p = np.zeros(N)  # Hole concentration (m^-3)
rho = np.zeros(N)  # Net charge density (C/m^3)
F = np.zeros(N)  # Fermi level (eV)

contact_mask = np.zeros(N, dtype=bool)

contact_size = 0.1
contact_width = int(contact_size * N) + 1
V[:contact_width] = 0.0
V[-contact_width:] = V_D
F[:contact_width] = E_B  # Set Fermi level at the contact to the barrier energy
F[-contact_width:] = E_B - e*V_D  # Set Fermi level at the contact to
contact_mask[:contact_width] = True
contact_mask[-contact_width:] = True

# # Depletion width estimation for initial guess
# W = np.sqrt(2 * epsilon * V_tot / (e * N_A))  # Depletion width in meters
# print(f"Estimated depletion width (W): {W*1e6:.2f} um")


def enter_pressed():
    if msvcrt is None:
        return False
    if not msvcrt.kbhit():
        return False
    while msvcrt.kbhit():
        if msvcrt.getwch() in ('\r', '\n'):
            return True
    return False


def time_format(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def solve():
    global V, rho, p, F

    contact_V = V.copy()
    alpha = 0.05
    error = np.zeros(iter)

    print("Press Enter in the terminal to stop the iteration early.")

    for i in range(iter):
        F = E_B - e*V_D*(x - (contact_width-1)*dx)/((N-2*contact_width+1)*dx)
        p = N_A * np.exp(-(V - V_tot + F/e) / V_T)  # Hole concentration using Boltzmann approximation
        p[:contact_width-1] = 0  # Zero only the contact region; other entries stay unchanged
        # p[contact_width-1] = p_edge  # Set the hole concentration at the edge of the depletion region
        rho[:contact_width-1] = 0  # Ensure the contact region has zero net charge
        p[-contact_width+1:] = 0  # Ensure the other contact region has zero hole
        rho[-contact_width+1:] = 0  # Ensure the other contact region has zero net charge
        rho = e * (p - N_A)  # Net charge density (C/m^3)


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

        if error[i] <= 5e-13:
            elapsed_time = time.time() - start_time
            print(f"Converged at iteration: {i + 1}/{iter}, Error: {error[i]:.2e} %, Runtime: {time_format(elapsed_time)}")
            error = error[:i + 1]
            break

        if enter_pressed():
            elapsed_time = time.time() - start_time
            print(f"Stopped by User at iteration: {i + 1}/{iter}, Error: {error[i]:.2e} %, Runtime: {time_format(elapsed_time)}")
            error = error[:i + 1]
            break

        if (i + 1) % step_iter == 0:
            elapsed_time = time.time() - start_time
            print(f"Iteration: {i + 1}/{iter}, Error: {error[i]:.2e} %, Runtime: {time_format(elapsed_time)}\r", end="")
        
    return V, rho, F

V, rho, F = solve()
np.savetxt("./Data-Export/ohmic_Poti_" + File_index + ".dat", V)
np.savetxt("./Data-Export/ohmic_Dens_" + File_index + ".dat", rho)

E = -np.gradient(V, dx)
dp_dx = np.gradient(p, dx)



fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

ax1.plot(x * 1e6, -V, color='blue', lw=2)
ax1.plot([0,(contact_width-1) * dx * 1e6],[F[0]/e, F[contact_width-1]/e], color='blue', lw=2, ls='--')
ax1.plot([(N - contact_width) * dx * 1e6, L * 1e6], [F[-contact_width]/e, F[-1]/e], color='blue', lw=2, ls='--')
ax1.plot(F/e, color='blue', lw=2, ls='--')
ax1.axhline(0, color='black', linestyle='--')
# ax1.axhline(V_tot, color='black', linestyle='--')
ax1.axhline(V_D, color='black', linestyle='--')
# ax1.plot([(contact_width-1) * dx * 1e6, (N - contact_width) * dx * 1e6], [V_G, V_D+V_G], color='black', linestyle='--', label='0 V')
ax1.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='--')
ax1.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='--')
ax1.set_ylabel('Energy (eV)')
ax1.set_title('Ohmic Contact (p-type) Simulation', fontsize=18)
ax1.set_xlim(0, L * 1e6)
ax1.set_ylim(-0.2, 0.2)

ax2.plot(x * 1e6, p, color='red', lw=2)
ax2.axhline(N_A, color='black', linestyle='--')
ax2.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='--')
ax2.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='--')
ax2.set_xlabel('Position (um)')
ax2.set_ylabel('Hole Concentration (m^-3)')
ax2.set_xlim(0, L * 1e6)
ax2.set_ylim(0, np.max(p) * 1.5)

# fig, (ax3, ax4) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

# ax3.plot(x * 1e6, E, color='green', lw=2)
# ax3.axhline(0, color='black', linestyle='--')
# ax3.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='--')
# ax3.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='--')
# ax3.set_ylabel('Electric Field (V/m)')

# ax4.plot(x * 1e6, dp_dx, color='purple', lw=2)
# ax4.axhline(0, color='black', linestyle='--')
# ax4.axvline((contact_width-1) * dx * 1e6, color='black', linestyle='--')
# ax4.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='--')
# ax4.set_xlabel('Position (um)')
# ax4.set_ylabel('dp/dx (m$^{-4}$)')
# ax4.set_xlim(0, L * 1e6)
fig.tight_layout()
plt.show()
