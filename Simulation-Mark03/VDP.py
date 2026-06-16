"""
VDP.py
------
2D gated van-der-Pauw / FET drift-diffusion + Poisson simulation.

This file is adapted from the 1D MOSFET.py model and uses the 2D
finite-difference Poisson update style of poisson-09-new.py.

Main equations
--------------
Hole density:
    p = N_v exp[-(F + e phi - e V_G)/(k_B T)]

Poisson equation:
    div(grad(phi)) = -rho/epsilon,  rho = e (p - N_A)

Steady-state hole continuity in conservative form:
    div(p grad(F)) = 0

The quasi-Fermi level F is stored in joule. It is exported in eV.
The in-plane current density is
    J = mu p grad(F)
which is equivalent to the drift-diffusion expression for the chosen
Boltzmann carrier density.
"""

import os
import time

import matplotlib.pyplot as plt
import numpy as np

try:
    import msvcrt
except ImportError:  # Linux/macOS/Jupyter
    msvcrt = None

# ----------------------------------------------------------------------
# Plot style
# ----------------------------------------------------------------------
plt.style.use("classic")
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["axes.edgecolor"] = "black"
plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams["savefig.facecolor"] = "white"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial"]
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["figure.dpi"] = 100

# ----------------------------------------------------------------------
# User parameters
# ----------------------------------------------------------------------
File_index = "01"

N = 101                      # grid points in x and y direction
L = 1000e-9                   # square side length [m]
max_iter = 1000000000            # increase for stricter convergence
step_iter = 10             # print interval
tolerance_percent = 5e-10    # stopping threshold for relative update error [%]

SAVE_RESULTS = True
PLOT_RESULTS = True
OUTPUT_DIR = "./Data-Export/VDP"

# Relaxation parameters. Smaller alpha_V is more stable for nonlinear Poisson.
alpha_V = 0.02
alpha_F = 0.15

# Contact geometry: four small square corner regions.
# Current is injected/sunk between contacts 1 and 2; contacts 3 and 4 are
# passive probe regions for reading V3 and V4.
contact_size = 0.08          # fraction of side length
contact_width = max(2, int(contact_size * N))

# ----------------------------------------------------------------------
# Physical constants and material parameters
# ----------------------------------------------------------------------
k_B = 1.380649e-23           # Boltzmann constant [J/K]
T = 300.0                    # temperature [K]
e = 1.602176634e-19          # elementary charge [C]
epsilon = 3.0 * 8.854187817e-12
mu = 1e-4                    # hole mobility [m^2/(V s)] = 1 cm^2/(V s)

Vth = k_B * T / e

# Voltages
V_bi = 5.0 * Vth            # built-in potential [V]
V_D = -10.0 * Vth            # contact-2 voltage relative to contact 1 [V]
V_G = 0.0 * Vth              # uniform gate voltage [V]

# Semiconductor parameters
N_A = 1e21                   # acceptor / neutral background density [m^-3]
N_v = 1e25                   # effective valence DOS [m^-3]

# Choose F boundary such that at contact 1 with phi=0:
# p_contact1 = Nv exp[-(F_contact1 - e V_G)/(kBT)] = NA exp(V_bi/Vth)
E_B = e * Vth * np.log(N_v / N_A) - e * V_bi  # [J]
p_contact1 = N_v * np.exp(-(E_B - e * V_G) / (k_B * T))

# ----------------------------------------------------------------------
# Grid and arrays
# ----------------------------------------------------------------------
x = np.linspace(0.0, L, N)
y = np.linspace(0.0, L, N)
dx = x[1] - x[0]
dy = y[1] - y[0]
X, Y = np.meshgrid(x, y)

V = np.zeros((N, N))         # electrostatic potential phi [V]
F = np.zeros((N, N))         # hole quasi-Fermi level [J]
p = np.zeros((N, N))         # hole density [m^-3]
rho = np.zeros((N, N))       # space charge density [C/m^3]

# Coordinate convention for masks: array index [iy, ix]
contact_1 = np.zeros((N, N), dtype=bool)  # bottom-left, injecting/source contact
contact_2 = np.zeros((N, N), dtype=bool)  # top-left, sinking/drain contact
contact_3 = np.zeros((N, N), dtype=bool)  # top-right, voltage probe
contact_4 = np.zeros((N, N), dtype=bool)  # bottom-right, voltage probe

cw = contact_width
contact_1[:cw, :cw] = True
contact_2[-cw:, :cw] = True
contact_3[-cw:, -cw:] = True
contact_4[:cw, -cw:] = True

# Only the two current contacts are Dirichlet boundaries in this model.
# The two probe contacts are used only to read local potentials, so they do
# not draw current and are not forced to a fixed quasi-Fermi level.
dirichlet_mask = contact_1 | contact_2
active_mask = ~dirichlet_mask

# Dirichlet boundary values at the two current contacts.
V_contact1 = 0.0
V_contact2 = V_D
F_contact1 = E_B
F_contact2 = E_B - e * V_D   # positive contact voltage lowers hole quasi-Fermi level

V[contact_1] = V_contact1
V[contact_2] = V_contact2
F[contact_1] = F_contact1
F[contact_2] = F_contact2

# Store the fixed boundary maps for easy re-application.
V_dirichlet = V.copy()
F_dirichlet = F.copy()

start_time = time.time()

print(f"Thermal voltage Vth: {Vth:.4f} V")
print(f"Built-in potential V_bi: {V_bi:.4f} V (={V_bi / Vth:.2f} Vth)")
print(f"Contact-2 voltage V_D: {V_D:.4f} V (={V_D / Vth:.2f} Vth)")
print(f"Gate voltage V_G: {V_G:.4f} V (={V_G / Vth:.2f} Vth)")
print(f"Barrier height E_B: {E_B / e:.4f} eV (={E_B / (k_B * T):.2f} kBT)")
print(f"Contact-1 hole concentration: {p_contact1:.3e} m^-3")
print(f"Grid: {N} x {N}, L = {L * 1e9:.1f} nm, contact width = {cw} pixels")


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def enter_pressed() -> bool:
    """Return True if Enter was pressed. Works on Windows terminals only."""
    if msvcrt is None:
        return False
    if not msvcrt.kbhit():
        return False
    while msvcrt.kbhit():
        if msvcrt.getwch() in ("\r", "\n"):
            return True
    return False


def time_format(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def safe_exp(arg: np.ndarray) -> np.ndarray:
    """Exponential with clipping to avoid numerical overflow."""
    return np.exp(np.clip(arg, -700.0, 700.0))


def carrier_density(F_map: np.ndarray, V_map: np.ndarray) -> np.ndarray:
    """Hole density p(F, phi, V_G)."""
    return N_v * safe_exp(-(F_map + e * V_map - e * V_G) / (k_B * T))


def harmonic_mean(a: np.ndarray, b: np.ndarray, tiny: float = 1e-300) -> np.ndarray:
    """Stable harmonic mean for face densities."""
    return 2.0 * a * b / (a + b + tiny)


def apply_neumann_edges(A: np.ndarray) -> None:
    """Zero normal derivative at the outer square boundary."""
    A[0, :] = A[1, :]
    A[-1, :] = A[-2, :]
    A[:, 0] = A[:, 1]
    A[:, -1] = A[:, -2]


def apply_dirichlet_contacts(A: np.ndarray, fixed_map: np.ndarray) -> None:
    """Re-apply fixed values at current contacts."""
    A[dirichlet_mask] = fixed_map[dirichlet_mask]


def update_F_conservative_2d(F_map: np.ndarray, p_map: np.ndarray) -> np.ndarray:
    """
    One relaxed Jacobi update of the 2D continuity equation

        div(p grad(F)) = 0.

    The finite-volume discretization uses harmonic means for p on cell faces.
    For a square grid with dx = dy, the update is a weighted average of the
    neighbouring quasi-Fermi levels.
    """
    F_candidate = F_map.copy()
    center = p_map[1:-1, 1:-1]

    p_e = harmonic_mean(center, p_map[1:-1, 2:])
    p_w = harmonic_mean(center, p_map[1:-1, :-2])
    p_n = harmonic_mean(center, p_map[2:, 1:-1])
    p_s = harmonic_mean(center, p_map[:-2, 1:-1])

    denom = p_e + p_w + p_n + p_s + 1e-300
    F_candidate[1:-1, 1:-1] = (
        p_e * F_map[1:-1, 2:]
        + p_w * F_map[1:-1, :-2]
        + p_n * F_map[2:, 1:-1]
        + p_s * F_map[:-2, 1:-1]
    ) / denom

    apply_neumann_edges(F_candidate)
    apply_dirichlet_contacts(F_candidate, F_dirichlet)

    F_relaxed = F_map.copy()
    F_relaxed[active_mask] = (1.0 - alpha_F) * F_map[active_mask] + alpha_F * F_candidate[active_mask]
    apply_dirichlet_contacts(F_relaxed, F_dirichlet)
    return F_relaxed


def compute_current_density(F_map: np.ndarray, p_map: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return Jx, Jy, and |J| from J = mu p grad(F)."""
    dF_dy, dF_dx = np.gradient(F_map, dy, dx)
    Jx = mu * p_map * dF_dx
    Jy = mu * p_map * dF_dy
    Jabs = np.sqrt(Jx**2 + Jy**2)
    return Jx, Jy, Jabs


def estimate_source_current_per_thickness(F_map: np.ndarray, p_map: np.ndarray) -> float:
    """
    Approximate total current emitted by contact 1 per film thickness [A/m].

    The source contact is the bottom-left square. Current leaves it through its
    top and right sides. This estimate is useful as a diagnostic for a
    voltage-driven simulation, but the main unknowns remain V, F, p and J.
    """
    c = cw

    # Right edge of contact 1: normal direction +x
    p_right = harmonic_mean(p_map[:c, c - 1], p_map[:c, c])
    dF_dx_right = (F_map[:c, c] - F_map[:c, c - 1]) / dx
    Jx_right = mu * p_right * dF_dx_right
    I_right = np.sum(Jx_right) * dy

    # Top edge of contact 1: normal direction +y
    p_top = harmonic_mean(p_map[c - 1, :c], p_map[c, :c])
    dF_dy_top = (F_map[c, :c] - F_map[c - 1, :c]) / dy
    Jy_top = mu * p_top * dF_dy_top
    I_top = np.sum(Jy_top) * dx

    return I_right + I_top


# ----------------------------------------------------------------------
# Main solver
# ----------------------------------------------------------------------
def solve() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, int, float]:
    global V, F, p, rho

    error = np.zeros(max_iter)
    elapsed_time = 0.0

    print("Press Enter in a Windows terminal to stop early.")

    for it in range(max_iter):
        V_old = V.copy()
        F_old = F.copy()

        # 1) Carrier density from quasi-Fermi level and electrostatic potential.
        p = carrier_density(F, V)

        # 2) Space charge only in the semiconductor region.
        rho[:] = 0.0
        rho[active_mask] = e * (p[active_mask] - N_A)

        # 3) 2D Poisson update: phi_xx + phi_yy = -rho/epsilon.
        V_candidate = V.copy()
        V_candidate[1:-1, 1:-1] = 0.25 * (
            V[2:, 1:-1]
            + V[:-2, 1:-1]
            + V[1:-1, 2:]
            + V[1:-1, :-2]
            + dx**2 * rho[1:-1, 1:-1] / epsilon
        )

        apply_neumann_edges(V_candidate)
        apply_dirichlet_contacts(V_candidate, V_dirichlet)

        V[active_mask] = (1.0 - alpha_V) * V[active_mask] + alpha_V * V_candidate[active_mask]
        apply_dirichlet_contacts(V, V_dirichlet)

        # 4) Continuity update using updated V.
        p = carrier_density(F, V)
        F = update_F_conservative_2d(F, p)

        # 5) Combined relative update error.
        err_V = np.max(np.abs(V - V_old)) / max(np.max(np.abs(V_old)), 1e-30)
        err_F = np.max(np.abs(F - F_old)) / max(np.max(np.abs(F_old)), 1e-30)
        error[it] = 100.0 * max(err_V, err_F)

        if error[it] <= tolerance_percent:
            elapsed_time = time.time() - start_time
            print(
                f"\nConverged at iteration {it + 1}/{max_iter}, "
                f"Error: {error[it]:.2e} %, Runtime: {time_format(elapsed_time)}"
            )
            return V, rho, F, p, error[: it + 1], it + 1, elapsed_time

        if enter_pressed():
            elapsed_time = time.time() - start_time
            print(
                f"\nStopped by user at iteration {it + 1}/{max_iter}, "
                f"Error: {error[it]:.2e} %, Runtime: {time_format(elapsed_time)}"
            )
            return V, rho, F, p, error[: it + 1], it + 1, elapsed_time

        if (it + 1) % step_iter == 0:
            elapsed_time = time.time() - start_time
            print(
                f"\rIteration: {it + 1}/{max_iter}, "
                f"Error: {error[it]:.2e} %, Runtime: {time_format(elapsed_time)}",
                end="",
                flush=True,
            )

    elapsed_time = time.time() - start_time
    print(
        f"\nReached max_iter = {max_iter}, "
        f"Error: {error[-1]:.2e} %, Runtime: {time_format(elapsed_time)}"
    )
    return V, rho, F, p, error, max_iter, elapsed_time


# ----------------------------------------------------------------------
# Run simulation
# ----------------------------------------------------------------------
V, rho, F, p, error, n_iterations, elapsed_time = solve()


# Final densities and current density.
p = carrier_density(F, V)
# rho[:] = 0.0
p_metal = 1e-10  # small but nonzero hole density in metal contacts to avoid NaNs
p[contact_1] = p_metal
p[contact_2] = p_metal
p[contact_3] = p_metal
p[contact_4] = p_metal

rho[active_mask] = e * (p[active_mask] - N_A)
Jx, Jy, Jabs = compute_current_density(F, p)
Jabs_metal = 1e-1  # small but nonzero current density in metal contacts for visualization
Jabs[contact_1] = Jabs_metal  # nonzero current density in metal contacts for visualization
Jabs[contact_2] = Jabs_metal
Jabs[contact_3] = Jabs_metal
Jabs[contact_4] = Jabs_metal

V3 = float(np.mean(V[contact_3]))
V4 = float(np.mean(V[contact_4]))
V34 = V3 - V4
I_source_per_thickness = estimate_source_current_per_thickness(F, p)

print(f"\nProbe potential V3: {V3:.6e} V")
print(f"Probe potential V4: {V4:.6e} V")
print(f"Probe voltage V3 - V4: {V34:.6e} V")
print(f"Estimated source current per film thickness: {I_source_per_thickness:.6e} A/m")
print(f"Mean |J| in active region: {np.mean(Jabs[active_mask]):.6e} A/m^2")

# ----------------------------------------------------------------------
# Save data
# ----------------------------------------------------------------------
if SAVE_RESULTS:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    np.savetxt(f"{OUTPUT_DIR}/VDP_Poti_{File_index}.dat", V)
    np.savetxt(f"{OUTPUT_DIR}/VDP_Fermi_eV_{File_index}.dat", F / e)
    np.savetxt(f"{OUTPUT_DIR}/VDP_Holes_{File_index}.dat", p)
    np.savetxt(f"{OUTPUT_DIR}/VDP_SpaceCharge_{File_index}.dat", rho)
    np.savetxt(f"{OUTPUT_DIR}/VDP_CurrentDensity_X_{File_index}.dat", Jx)
    np.savetxt(f"{OUTPUT_DIR}/VDP_CurrentDensity_Y_{File_index}.dat", Jy)
    np.savetxt(f"{OUTPUT_DIR}/VDP_CurrentDensity_Abs_{File_index}.dat", Jabs)
    np.savetxt(f"{OUTPUT_DIR}/VDP_Error_{File_index}.dat", error)

    log_lines = [
        "Title: 2D gated van-der-Pauw / FET simulator",
        f"Python file: {os.path.basename(__file__)}",
        f"Date and time: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Grid points: {N} x {N}",
        f"Device size: {L * 1e9:.2f} nm x {L * 1e9:.2f} nm",
        f"Contact width: {contact_width} pixels ({contact_width * dx * 1e9:.2f} nm)",
        f"Iterations performed: {n_iterations}",
        f"Runtime: {time_format(elapsed_time)}",
        "------------------------------------------------------",
        f"Thermal voltage: {Vth:.6f} V",
        f"Built-in voltage: {V_bi:.6f} V (={V_bi / Vth:.2f} Vth)",
        f"Gate voltage: {V_G:.6f} V (={V_G / Vth:.2f} Vth)",
        f"Contact-2 voltage: {V_D:.6f} V (={V_D / Vth:.2f} Vth)",
        f"Barrier height: {E_B / e:.6f} eV (={E_B / (k_B * T):.2f} kBT)",
        f"Contact-1 hole concentration: {p_contact1:.6e} m^-3",
        f"Acceptor/background density: {N_A:.2e} m^-3",
        f"Valence DOS: {N_v:.2e} m^-3",
        f"Mobility: {mu:.2e} m^2/(V s)",
        f"Permittivity: {epsilon:.6e} F/m",
        "------------------------------------------------------",
        f"Probe V3: {V3:.6e} V",
        f"Probe V4: {V4:.6e} V",
        f"Probe V3 - V4: {V34:.6e} V",
        f"Estimated source current per thickness: {I_source_per_thickness:.6e} A/m",
        f"Mean |J| active region: {np.mean(Jabs[active_mask]):.6e} A/m^2",
    ]

    with open(f"{OUTPUT_DIR}/VDP_log_{File_index}.txt", "w", encoding="utf-8") as log_file:
        log_file.write("\n".join(log_lines) + "\n")

# ----------------------------------------------------------------------
# Plotting
# ----------------------------------------------------------------------
if PLOT_RESULTS:
    x_nm = x * 1e9
    y_nm = y * 1e9
    extent_nm = [x_nm.min(), x_nm.max(), y_nm.min(), y_nm.max()]

    # Potential map
    fig_pot= plt.figure(figsize=(10, 8), constrained_layout=True)
    gs_pot = fig_pot.add_gridspec(1, 2, width_ratios=[1, 1.05])

    ax2D_pot = fig_pot.add_subplot(gs_pot[0, 0])
    im_pot = ax2D_pot.imshow(
        V,
        extent=extent_nm,
        origin="lower",
        interpolation="bicubic",
        aspect="equal",
    )
    fig_pot.colorbar(im_pot, ax=ax2D_pot, label=r"$\phi$ [V]", shrink=0.4)
    # ax2D_pot.contour(X * 1e9, Y * 1e9, V, levels=12, colors="k", linewidths=0.5)
    ax2D_pot.set_xlabel("x-position [nm]")
    ax2D_pot.set_ylabel("y-position [nm]")
    ax2D_pot.set_title("2D electrostatic potential")

    ax3D_pot = fig_pot.add_subplot(gs_pot[0, 1], projection="3d")
    surf_pot = ax3D_pot.plot_surface(
        X * 1e9,
        Y * 1e9,
        V,
        cmap="jet",
        rcount=N // 3,
        ccount=N // 3,
        linewidth=1,
        color="k",
        antialiased=True,
    )
    fig_pot.colorbar(surf_pot, ax=ax3D_pot, label=r"$\phi$ [V]", shrink=0.4, pad=0.08)  
    ax3D_pot.set_xlabel("x-position [nm]")
    ax3D_pot.set_ylabel("y-position [nm]")
    ax3D_pot.set_zlabel(r"$\phi$ [V]")
    ax3D_pot.set_title("3D electrostatic potential")
    
    fig_pot.suptitle("Electrostatic Potential Distribution")

    # Hole density map
    fig_hole = plt.figure(figsize=(10, 8), constrained_layout=True)
    gs_hole = fig_hole.add_gridspec(1, 2, width_ratios=[1, 1.05])
    
    ax2D_hole = fig_hole.add_subplot(gs_hole[0, 0])
    im_hole = ax2D_hole.imshow(
        np.log10(np.maximum(p, 1.0)),
        extent=extent_nm,
        origin="lower",
        interpolation="bicubic",
        aspect="equal",
    )
    fig_hole.colorbar(im_hole, ax=ax2D_hole, label=r"$\log_{10}(p/\mathrm{m}^{-3})$", shrink=0.4)
    ax2D_hole.set_xlabel("x-position [nm]")
    ax2D_hole.set_ylabel("y-position [nm]")
    ax2D_hole.set_title("2D hole density")

    ax3D_hole = fig_hole.add_subplot(gs_hole[0, 1], projection="3d")
    surf_hole = ax3D_hole.plot_surface(
        X * 1e9,
        Y * 1e9,    
        np.log10(np.maximum(p, 1.0)),
        cmap="jet",
        rcount=N // 3,
        ccount=N // 3,
        linewidth=1,
        color="k",
        antialiased=True,
    )
    fig_hole.colorbar(surf_hole, ax=ax3D_hole, label=r"$\log_{10}(p/\mathrm{m}^{-3})$", shrink=0.4, pad=0.08)
    ax3D_hole.set_xlabel("x-position [nm]")
    ax3D_hole.set_ylabel("y-position [nm]")
    ax3D_hole.set_zlabel(r"$\log_{10}(p/\mathrm{m}^{-3})$")
    ax3D_hole.set_title("3D hole density")
    fig_hole.suptitle("Hole Density Distribution")

    # Current streamlines and magnitude
    fig_J = plt.figure(figsize=(10, 8), constrained_layout=True)
    gs_J = fig_J.add_gridspec(1, 2, width_ratios=[1, 1.05])
    ax2D_J = fig_J.add_subplot(gs_J[0, 0])

    im_J = ax2D_J.imshow(
        np.log10(np.maximum(Jabs, 1e-300)),
        extent=extent_nm,
        origin="lower",
        interpolation="bicubic",
        aspect="equal",
    )
    fig_J.colorbar(im_J, ax=ax2D_J, label=r"$\log_{10}|J|$ [A/m$^2$]", shrink=0.4)
    ax2D_J.set_xlabel("x-position [nm]")
    ax2D_J.set_ylabel("y-position [nm]")
    ax2D_J.set_title("Current density magnitude and streamlines")

    ax3D_J = fig_J.add_subplot(gs_J[0, 1], projection="3d")
    surf_J = ax3D_J.plot_surface(
        X * 1e9,
        Y * 1e9,
        np.log10(np.maximum(Jabs, 1e-300)),
        cmap="jet",
        rcount=N // 3,
        ccount=N // 3,
        linewidth=1,
        color="k",
        antialiased=True,
    )
    fig_J.colorbar(surf_J, ax=ax3D_J, label=r"$\log_{10}|J|$ [A/m$^2$]", shrink=0.4, pad=0.08)
    ax3D_J.set_xlabel("x-position [nm]")
    ax3D_J.set_ylabel("y-position [nm]")
    ax3D_J.set_zlabel(r"$\log_{10}|J|$ [A/m$^2$]")
    ax3D_J.set_title("3D current density magnitude")
    fig_J.suptitle("Current Density Distribution")

    plt.show()
