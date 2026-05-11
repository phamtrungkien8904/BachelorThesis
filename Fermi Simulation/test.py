import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expit

# -----------------------------
# constants
# -----------------------------
q = 1.602176634e-19
eps0 = 8.8541878128e-12
kB = 1.380649e-23
T = 300
Vt = kB * T / q

# -----------------------------
# grid, similar to documentation: 51 x 51 x 101
# -----------------------------
Nx, Ny, Nz = 51, 51, 101
n_outer = 25
n_sor = 60
omega = 1.5
tol = 1e-4
Lx, Ly, Lz = 50e-9, 50e-9, 100e-9

dx = Lx / (Nx - 1)
dy = Ly / (Ny - 1)
dz = Lz / (Nz - 1)

x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)
z = np.linspace(0, Lz, Nz)

X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

# -----------------------------
# material stack
# bottom: gate
# middle: insulator
# top: semiconductor
# -----------------------------
z_interface = 60e-9

is_ins = Z < z_interface
is_sem = Z >= z_interface

eps_r = np.zeros((Nx, Ny, Nz))
eps_r[is_ins] = 2.5       # e.g. polystyrene
eps_r[is_sem] = 3.0       # organic semiconductor

eps = eps0 * eps_r

# -----------------------------
# semiconductor DOS parameters
# -----------------------------
N_HOMO = 1e25       # m^-3 = 1e19 cm^-3
V0 = -2.5           # effective HOMO-Fermi offset in volt units
Vt_eff = 0.20       # broadened FD width, organic disorder > 25.9 mV

def hole_density(phi):
    """
    Fermi-Dirac-like hole density.
    More negative phi -> HOMO moves up -> more holes.
    """
    eta = (V0 - phi) / Vt_eff
    return N_HOMO * expit(eta)

def charge_density(phi):
    rho = np.zeros_like(phi)
    rho[is_sem] = q * hole_density(phi[is_sem])
    return rho

# -----------------------------
# boundary conditions
# -----------------------------
def make_dirichlet_masks(VG4=-5.0, V34=0.0):
    """
    Set contact 4 = 0 V.
    Set gate = VG4.
    Set contact 3 = V34.
    """
    fixed = np.zeros((Nx, Ny, Nz), dtype=bool)
    value = np.zeros((Nx, Ny, Nz))

    # bottom gate plane
    gate = Z[:, :, 0] == z[0]
    fixed[:, :, 0] = True
    value[:, :, 0] = VG4

    # top semiconductor surface
    ktop = Nz - 1

    # contact 4: left top strip
    c4 = (X[:, :, ktop] < 6e-9) & (Y[:, :, ktop] > 15e-9) & (Y[:, :, ktop] < 35e-9)
    fixed[:, :, ktop][c4] = True
    value[:, :, ktop][c4] = 0.0

    # contact 3: right top strip
    c3 = (X[:, :, ktop] > 44e-9) & (Y[:, :, ktop] > 15e-9) & (Y[:, :, ktop] < 35e-9)
    fixed[:, :, ktop][c3] = True
    value[:, :, ktop][c3] = V34

    return fixed, value

# -----------------------------
# nonlinear Poisson solver
# Picard + SOR
# -----------------------------
def solve_poisson_fd(VG4=-5.0, V34=0.0, n_outer=n_outer, n_sor=n_sor, omega=omega):
    fixed, fixed_val = make_dirichlet_masks(VG4, V34)

    # initial guess: vertical interpolation between gate and 0 V
    phi = np.zeros((Nx, Ny, Nz))
    for k in range(Nz):
        alpha = z[k] / Lz
        phi[:, :, k] = (1 - alpha) * VG4 + alpha * 0.0

    phi[fixed] = fixed_val[fixed]

    for outer in range(n_outer):
        phi_old = phi.copy()
        rho = charge_density(phi)

        for _ in range(n_sor):

            # Neumann outer side boundaries
            phi[0, :, :] = phi[1, :, :]
            phi[-1, :, :] = phi[-2, :, :]
            phi[:, 0, :] = phi[:, 1, :]
            phi[:, -1, :] = phi[:, -2, :]
            phi[:, :, -1] = phi[:, :, -2]

            phi[fixed] = fixed_val[fixed]

            for i in range(1, Nx - 1):
                for j in range(1, Ny - 1):
                    for k in range(1, Nz - 1):
                        if fixed[i, j, k]:
                            continue

                        ae = 0.5 * (eps[i, j, k] + eps[i+1, j, k]) / dx**2
                        aw = 0.5 * (eps[i, j, k] + eps[i-1, j, k]) / dx**2
                        an = 0.5 * (eps[i, j, k] + eps[i, j+1, k]) / dy**2
                        as_ = 0.5 * (eps[i, j, k] + eps[i, j-1, k]) / dy**2
                        au = 0.5 * (eps[i, j, k] + eps[i, j, k+1]) / dz**2
                        ad = 0.5 * (eps[i, j, k] + eps[i, j, k-1]) / dz**2

                        denom = ae + aw + an + as_ + au + ad

                        phi_new = (
                            ae * phi[i+1, j, k] +
                            aw * phi[i-1, j, k] +
                            an * phi[i, j+1, k] +
                            as_ * phi[i, j-1, k] +
                            au * phi[i, j, k+1] +
                            ad * phi[i, j, k-1] +
                            rho[i, j, k]
                        ) / denom

                        phi[i, j, k] = (1 - omega) * phi[i, j, k] + omega * phi_new

        error = np.max(np.abs(phi - phi_old))
        print(f"outer {outer:03d}, error = {error:.3e} V")
        if error < 1e-5:
            break

    p = np.zeros_like(phi)
    p[is_sem] = hole_density(phi[is_sem])
    return phi, p

# -----------------------------
# run cases
# -----------------------------
phi_a, p_a = solve_poisson_fd(VG4=-5.0, V34=0.0)
phi_b, p_b = solve_poisson_fd(VG4=-5.0, V34=-4.0)

# interface slice: first semiconductor layer
k_int = np.where(z >= z_interface)[0][0]

p_a_cm3 = p_a[:, :, k_int] / 1e6
p_b_cm3 = p_b[:, :, k_int] / 1e6

# -----------------------------
# plot carrier density at semiconductor-insulator interface
# -----------------------------
X2, Y2 = np.meshgrid(x * 1e9, y * 1e9, indexing="ij")

fig = plt.figure(figsize=(9, 7))

ax = fig.add_subplot(2, 1, 1, projection="3d")
ax.plot_wireframe(X2, Y2, p_a_cm3 / 1e18, rstride=2, cstride=2)
ax.set_title(r"a) $V_{G4}=-5$ V, $V_{34}=0$ V")
ax.set_xlabel("x (nm)")
ax.set_ylabel("y (nm)")
ax.set_zlabel(r"$p$ ($10^{18}$ cm$^{-3}$)")

ax = fig.add_subplot(2, 1, 2, projection="3d")
ax.plot_wireframe(X2, Y2, p_b_cm3 / 1e18, rstride=2, cstride=2)
ax.set_title(r"b) $V_{G4}=-5$ V, $V_{34}=-4$ V")
ax.set_xlabel("x (nm)")
ax.set_ylabel("y (nm)")
ax.set_zlabel(r"$p$ ($10^{18}$ cm$^{-3}$)")

plt.tight_layout()
plt.show()

# -----------------------------
# potential along x between contacts 3 and 4
# -----------------------------
j_mid = Ny // 2

plt.figure(figsize=(7, 4))
plt.plot(x * 1e9, phi_a[:, j_mid, k_int], label=r"$V_{34}=0$ V")
plt.plot(x * 1e9, phi_b[:, j_mid, k_int], label=r"$V_{34}=-4$ V")
plt.xlabel("x (nm)")
plt.ylabel("potential $\\phi$ (V)")
plt.title(r"Potential at semiconductor-insulator interface, $V_{G4}=-5$ V")
plt.grid(True)
plt.legend()
plt.show()