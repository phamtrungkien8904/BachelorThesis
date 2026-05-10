import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Physical constants
# -----------------------------
q = 1.602176634e-19      # C
kB = 1.380649e-23        # J/K
T = 300                  # K
Vthermal = kB * T / q    # about 25.9 mV

# -----------------------------
# Device / material parameters
# -----------------------------
Lx = 50e-9               # 50 nm
Ly = 50e-9               # 50 nm
Nx = 101
Ny = 101

t_sc = 40e-9             # semiconductor thickness, 40 nm
mu = 1e-4                # m^2/Vs = 1 cm^2/Vs
Nmax = 1e26              # m^-3 = 1e20 cm^-3

# Organic semiconductor: broadened FD transition
# For ideal semiconductor use Vscale = Vthermal.
# For organic/disordered semiconductor use 0.05...0.2 V.
Vscale = 0.10

# Threshold voltage for p-type accumulation
Vth = -1.0

x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)
X, Y = np.meshgrid(x, y)


def hole_density_FD(Vch, VG):
    """
    Fermi-Dirac-like hole density.
    p-type convention:
    more negative (VG - Vch) => more holes.
    """
    arg = (VG - Vch - Vth) / Vscale
    arg = np.clip(arg, -80, 80)
    p = Nmax / (1.0 + np.exp(arg))
    return p


def solve_gvdp_case(VG4=-5.0, V34=0.0, max_iter=8000, tol=1e-8):
    """
    Thin-film gVDP interface model.

    We set:
        V4 = 0
        VG = VG4
        V3 = V34

    Contacts 4 and 3 are represented as left and right contact strips.
    """
    VG = VG4
    V4 = 0.0
    V3 = V34

    # Initial potential: linear interpolation between contacts
    V = np.tile(np.linspace(V4, V3, Nx), (Ny, 1))

    # Contact masks
    contact_width = 2e-9
    contact4 = X < contact_width
    contact3 = X > (Lx - contact_width)

    fixed = contact3 | contact4
    fixed_value = np.zeros_like(V)
    fixed_value[contact4] = V4
    fixed_value[contact3] = V3

    # Small floor conductivity to avoid division by zero
    sigma_floor = 1e-14

    omega = 1.2  # relaxation factor

    for it in range(max_iter):
        V_old = V.copy()

        # Neumann boundary on top/bottom: dV/dn = 0
        V[0, :] = V[1, :]
        V[-1, :] = V[-2, :]

        # Dirichlet contacts
        V[fixed] = fixed_value[fixed]

        # Local carrier density from Fermi-Dirac-like law
        p = hole_density_FD(V, VG)

        # Sheet conductivity
        sigma = q * mu * t_sc * p + sigma_floor

        # Conductivities at half-grid positions
        sig_c = sigma[1:-1, 1:-1]
        sig_e = 0.5 * (sig_c + sigma[1:-1, 2:])
        sig_w = 0.5 * (sig_c + sigma[1:-1, :-2])
        sig_n = 0.5 * (sig_c + sigma[2:, 1:-1])
        sig_s = 0.5 * (sig_c + sigma[:-2, 1:-1])

        denominator = sig_e + sig_w + sig_n + sig_s

        V_new_inner = (
            sig_e * V[1:-1, 2:] +
            sig_w * V[1:-1, :-2] +
            sig_n * V[2:, 1:-1] +
            sig_s * V[:-2, 1:-1]
        ) / denominator

        inner_fixed = fixed[1:-1, 1:-1]
        V_inner = V[1:-1, 1:-1]
        V_inner[~inner_fixed] = (
            (1 - omega) * V_inner[~inner_fixed]
            + omega * V_new_inner[~inner_fixed]
        )
        V[1:-1, 1:-1] = V_inner

        V[fixed] = fixed_value[fixed]

        error = np.max(np.abs(V - V_old))
        if error < tol:
            break

    p = hole_density_FD(V, VG)
    return V, p, it


# -----------------------------
# Run two cases
# -----------------------------
V_a, p_a, it_a = solve_gvdp_case(VG4=-5.0, V34=0.0)
V_b, p_b, it_b = solve_gvdp_case(VG4=-5.0, V34=-4.0)

print("Iterations case a:", it_a)
print("Iterations case b:", it_b)

# Convert density from m^-3 to cm^-3
p_a_cm3 = p_a / 1e6
p_b_cm3 = p_b / 1e6

# -----------------------------
# 3D wireframe carrier density
# -----------------------------
fig = plt.figure(figsize=(10, 8))

ax1 = fig.add_subplot(2, 1, 1, projection="3d")
ax1.plot_wireframe(X * 1e9, Y * 1e9, p_a_cm3 / 1e18, rstride=4, cstride=4)
ax1.set_title(r"a) $V_{G4}=-5.0$ V, $V_{34}=0.0$ V")
ax1.set_xlabel("x (nm)")
ax1.set_ylabel("y (nm)")
ax1.set_zlabel(r"$p$ ($10^{18}$ cm$^{-3}$)")

ax2 = fig.add_subplot(2, 1, 2, projection="3d")
ax2.plot_wireframe(X * 1e9, Y * 1e9, p_b_cm3 / 1e18, rstride=4, cstride=4)
ax2.set_title(r"b) $V_{G4}=-5.0$ V, $V_{34}=-4.0$ V")
ax2.set_xlabel("x (nm)")
ax2.set_ylabel("y (nm)")
ax2.set_zlabel(r"$p$ ($10^{18}$ cm$^{-3}$)")

plt.tight_layout()
plt.show()

# -----------------------------
# Potential along x at middle y
# -----------------------------
mid = Ny // 2

plt.figure(figsize=(7, 4))
plt.plot(x * 1e9, V_a[mid, :], label=r"$V_{34}=0.0$ V")
plt.plot(x * 1e9, V_b[mid, :], label=r"$V_{34}=-4.0$ V")
plt.xlabel("x (nm)")
plt.ylabel("Potential V")
plt.title(r"Potential along x, $V_{G4}=-5.0$ V")
plt.legend()
plt.grid(True)
plt.show()