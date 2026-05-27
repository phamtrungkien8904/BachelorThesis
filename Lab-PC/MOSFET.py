import os
import time

import matplotlib.pyplot as plt
import numpy as np

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

# ----------------------------------------------------------------------
# Simulation parameters
# ----------------------------------------------------------------------
N = 201
max_iter = 2000000          # increase if needed
step_iter = 10
L = 100e-6
x = np.linspace(0, L, N)
dx = x[1] - x[0]

# Physical constants
k_B = 1.380649e-23
T = 300.0
e = 1.602176634e-19
epsilon = 3 * 8.854187817e-12
mu = 1e-4                    # hole mobility [m^2/(V s)] = 1 cm^2/(V s)

Vth = k_B * T / e
print(f"Thermal voltage kBT/e: {Vth:.4f} V")

# Voltages
V_bi = 2 * Vth               # built-in potential [V]
V_G = 0.0
                   # optional external/gate offset if you want later
V_D = 0.0                   # drain/contact voltage [V]

print(f"Built-in potential V_bi: {V_bi:.4f} V")
print(f"Drain voltage V_D: {V_D:.4f} V")
print(f"Gate voltage V_G: {V_G:.4f} V")
# Semiconductor parameters
N_A = 1e18                 # acceptor density [m^-3]
N_v = 1e19                   # effective DOS [m^-3]

# Choose F boundary such that at left contact phi=0:
# p_left = Nv * exp(-F_left/kBT) = NA * exp(V_bi/Vth)
E_B = k_B * T * (np.log(N_v / N_A) - V_bi / Vth)  # [J]
p_left = N_v * np.exp(-E_B / (k_B * T))
print(f"Left boundary Fermi energy E_B: {E_B/e:.4f} eV")
print(f"Left boundary hole density: {p_left:.3e} m^-3")

# ----------------------------------------------------------------------
# Arrays
# V   = electrostatic potential phi [V]
# F   = hole quasi-Fermi level [J]
# p   = hole density [m^-3]
# rho = space charge density [C/m^3]
# ----------------------------------------------------------------------
V = np.zeros(N)
F = np.zeros(N)
p = np.zeros(N)
rho = np.zeros(N)

# Contact regions
contact_size = 0.10
contact_width = int(contact_size * N) + 1
contact_mask = np.zeros(N, dtype=bool)
contact_mask[:contact_width] = True
contact_mask[-contact_width:] = True
active_mask = ~contact_mask

# Dirichlet boundary values at ohmic contacts
V_left = 0.0
V_right = V_D
F_left = E_B
F_right = E_B - e * V_D     # positive contact voltage lowers F by eV

V[:contact_width] = V_left
V[-contact_width:] = V_right
F[:contact_width] = F_left
F[-contact_width:] = F_right

# Enter key press detection for early stopping
def enter_pressed():
    if msvcrt is None:
        return False
    if not msvcrt.kbhit():
        return False
    while msvcrt.kbhit():
        if msvcrt.getwch() in ('\r', '\n'):
            return True
    return False

# Time formatting for runtime display
def time_format(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# Continuity update in conservative form: d/dx(p dF/dx) = 0
def update_F_conservative(F, V, p, alpha_F):
    """
    Solve continuity in conservative form:
        d/dx( p dF/dx ) = 0

    This is equivalent to the expanded equation:
        F'' - (1/kBT) * (F' + e*phi') * F' = 0
    when p = Nv exp(-(F + e phi)/kBT).
    """
    F_new = F.copy()

    # Face densities. Harmonic mean is stable when p changes strongly.
    tiny = 1e-300
    p_e = 2 * p[1:-1] * p[2:] / (p[1:-1] + p[2:] + tiny)
    p_w = 2 * p[1:-1] * p[:-2] / (p[1:-1] + p[:-2] + tiny)

    F_new[1:-1] = (p_e * F[2:] + p_w * F[:-2]) / (p_e + p_w + tiny)

    # Dirichlet quasi-Fermi level at ohmic contacts
    F_new[:contact_width] = F_left
    F_new[-contact_width:] = F_right

    return (1 - alpha_F) * F + alpha_F * F_new


def solve():
    global V, F, p, rho

    alpha_V = 0.05
    alpha_F = 0.2
    error = np.zeros(max_iter)

    print("Press Enter in the terminal to stop early.")

    for it in range(max_iter):
        V_old = V.copy()
        F_old = F.copy()
        
        p[:contact_width-1] =0
        p[-contact_width:]=0    

        # 1) carrier density from quasi-Fermi level and electrostatic potential
        p = N_v * np.exp(-(F + e * V - e *V_G) / (k_B * T))

        # 2) space charge only in semiconductor region; contacts are fixed reservoirs
        rho[:] = 0.0
        rho[active_mask] = e * (p[active_mask] - N_A)

        # 3) Poisson update: phi'' = -rho/epsilon
        V_new = V.copy()
        V_new[1:-1] = 0.5 * (V[:-2] + V[2:] + dx**2 * rho[1:-1] / epsilon)

        # Dirichlet electrostatic potential at contacts
        V_new[:contact_width] = V_left
        V_new[-contact_width:] = V_right

        # Optional Neumann boundaries are irrelevant here because contacts touch edges,
        # but keep them safe if contact_width is changed to 0 in future.
        if contact_width == 0:
            V_new[0] = V_new[1]
            V_new[-1] = V_new[-2]

        V = (1 - alpha_V) * V + alpha_V * V_new

        # 4) Continuity update for quasi-Fermi level:
        #    d/dx(p dF/dx)=0
        #    Use updated V but p from previous step; recompute p before F update.
        p = N_v * np.exp(-(F + e * V) / (k_B * T))
        F = update_F_conservative(F, V, p, alpha_F)

        # 5) combined relative error
        err_V = np.max(np.abs(V - V_old)) / max(np.max(np.abs(V_old)), 1e-30)
        err_F = np.max(np.abs(F - F_old)) / max(np.max(np.abs(F_old)), 1e-30)
        error[it] = 100.0 * max(err_V, err_F)

        if error[it] <= 5e-13:
            elapsed_time = time.time() - start_time
            print(f"\nConverged at iteration: {it + 1}/{max_iter}, Error: {error[it]:.2e} %, Runtime: {time_format(elapsed_time)}")
            error = error[:it + 1]
            break

        if enter_pressed():
            elapsed_time = time.time() - start_time
            print(f"\nStopped by user at iteration: {it + 1}/{max_iter}, Error: {error[it]:.2e} %, Runtime: {time_format(elapsed_time)}")
            error = error[:it + 1]
            break


        if (it + 1) % step_iter == 0:
            elapsed_time = time.time() - start_time
            print(f"\rIteration: {it + 1}/{max_iter}, Error: {error[it]:.2e} %, Runtime: {time_format(elapsed_time)}", end="", flush=True)


    # final quantities
    p = N_v * np.exp(-(F + e * V) / (k_B * T))
    rho[:] = 0.0
    rho[active_mask] = e * (p[active_mask] - N_A)
    return V, rho, F, p


V, rho, F, p = solve()

# ----------------------------------------------------------------------
# Diagnostics: verify expanded equation
# F'' - 1/kBT * (F' + e phi') F' = 0
# ----------------------------------------------------------------------
dV_dx = np.gradient(V, dx)
y = np.gradient(F, dx)
dy_dx = np.gradient(y, dx)
J = mu * p * y  # from J = mu p dF/dx

print(f"Mean current density active region: {np.mean(J[active_mask]):.3e} A/m^2")

# ----------------------------------------------------------------------
# Save data
# ----------------------------------------------------------------------
os.makedirs("./Data-Export", exist_ok=True)
np.savetxt(f"./Data-Export/ohmic_Poti_{File_index}.dat", V)
np.savetxt(f"./Data-Export/ohmic_Dens_{File_index}.dat", rho)
np.savetxt(f"./Data-Export/ohmic_QuasiFermi_{File_index}.dat", F / e)  # eV
np.savetxt(f"./Data-Export/ohmic_Holes_{File_index}.dat", p)
np.savetxt(f"./Data-Export/ohmic_CurrentDensity_{File_index}.dat", J)

# ----------------------------------------------------------------------
# Plotting
# ----------------------------------------------------------------------
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

ax1.plot(x * 1e6, -V, color='blue', lw=2, label=r'$-\phi$ [V]')
ax1.plot(x * 1e6, F / e, color='blue', lw=2, ls='--', label=r'$F_p$ [eV]')
ax1.axhline(0, color='black', linestyle='--')
ax1.axhline(-V_bi, color='black', linestyle='--', label=r'$-V_{bi}$')
ax1.axvline((contact_width - 1) * dx * 1e6, color='black', linestyle='--')
ax1.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='--')
ax1.set_ylabel('Energy / potential')
ax1.set_title('Poisson + Continuity: quasi-Fermi level solved numerically', fontsize=16)
ax1.set_xlim(0, L * 1e6)

ax2.plot(x * 1e6, p, color='red', lw=2)
ax2.axhline(N_A, color='black', linestyle='--', label=r'$N_A$')
ax2.axvline((contact_width - 1) * dx * 1e6, color='black', linestyle='--')
ax2.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='--')
ax2.set_ylabel(r'$p$ [m$^{-3}$]')
ax2.set_ylim(0, np.nanmax(p) * 1.2)

ax3.plot(x * 1e6, J, color='green', lw=2)
ax3.axvline((contact_width - 1) * dx * 1e6, color='black', linestyle='--')
ax3.axvline((N - contact_width) * dx * 1e6, color='black', linestyle='--')
ax3.set_xlabel('Position [um]')
ax3.set_ylabel(r'$J$ [A/m$^2$]')

fig.tight_layout()
plt.show()
