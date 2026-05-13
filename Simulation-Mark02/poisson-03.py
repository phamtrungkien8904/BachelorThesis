import time
import numpy as np
import matplotlib.pyplot as plt

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

# Test
start_time = time.time()


kB = 1  # Boltzmann constant in J/K
T = 1
beta = 1 / (kB * T)
e = 1
E_F = 1.0
epsilon = 1

# HOMO
Nv =2.0  # effective HOMO DOS
Ev0 = 0.0


N = 101
iter = 100000

x = np.linspace(0, 1, N)
y = np.linspace(0, 1, N)
X, Y = np.meshgrid(x, y)


V = np.zeros((N, N))
rho = np.zeros((N, N))
p = np.zeros((N, N))
contact_mask = np.zeros((N, N), dtype=bool)


# Contact configuration (Schottky-injection)
contact_size = 0.1
contact_width = int(contact_size * N)
V[:contact_width, :contact_width] = 0.0
V[-contact_width:, :contact_width] = -5.0
rho[:contact_width, :contact_width] = 0.0
rho[-contact_width:, :contact_width] = 0.0
p[:contact_width, :contact_width] = 0.0
p[-contact_width:, :contact_width] = 0.0
contact_mask[:contact_width, :contact_width] = True
contact_mask[-contact_width:, :contact_width] = True

# Cross geometry
cross_mask = np.zeros((N, N), dtype=bool)

# Cross geometry
cross_width = 0.08
cw = int(cross_width * N)
half_cw = cw // 2
center = N // 2

# vertical arm
cross_mask[:, center-half_cw:center+half_cw+1] = True

# horizontal arm
cross_mask[center-half_cw:center+half_cw+1, :] = True

# masks
non_semiconductor_mask = contact_mask | cross_mask

# fixed-potential regions
fixed_mask = contact_mask | cross_mask



def solve():
    global V, rho, p

    dx = x[1] - x[0]

    # neutral bulk values at V = 0
    p0 = Nv / (1 + np.exp(np.clip(beta * (E_F - Ev0), -100, 100)))

    alpha = 0.05

    for i in range(iter):

        # All electron energy levels shift as E = E0 - eV
        Ev = Ev0 - e * V

        # hole density
        p = Nv / (
            1 + np.exp(np.clip(beta * (E_F - Ev), -100, 100))
        )

        # net charge density referenced to the neutral equilibrium bulk
        rho = e * (p - p0)

        # no semiconductor charge inside metal/contact/cross region
        rho[non_semiconductor_mask] = 0.0
        p[non_semiconductor_mask] = 0.0


        # Poisson update
        V_new = V.copy()

        V_new[1:-1, 1:-1] = 0.25 * (
            V[2:, 1:-1]
            + V[:-2, 1:-1]
            + V[1:-1, 2:]
            + V[1:-1, :-2]
            + dx**2 * rho[1:-1, 1:-1] / epsilon
        )

        # Neumann outer boundaries
        V_new[0, :] = V_new[1, :]
        V_new[-1, :] = V_new[-2, :]
        V_new[:, 0] = V_new[:, 1]
        V_new[:, -1] = V_new[:, -2]

        # Dirichlet contacts
        V_new[contact_mask] = V[contact_mask]

        # relaxation
        error = np.max(np.abs(V_new - V))
        V = (1 - alpha) * V + alpha * V_new

        if (i + 1) % 5000 == 0:
            print(f"Step {i + 1}/{iter}, Error: {error:.6e}")

    return V, rho, p

V, rho, p = solve()

end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds.")

fig2D_density = plt.figure(figsize=(8, 6))
ax2D = fig2D_density.add_subplot(111)
density_image = ax2D.imshow(
    p,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='viridis',
    interpolation='bicubic', # 'nearest' for exact grid values, 'bicubic' for smooth visualization
    vmin=p.min(),
    vmax=p.max()
)
fig2D_density.colorbar(density_image, ax=ax2D)
ax2D.set_xlabel('X-axis')
ax2D.set_ylabel('Y-axis')
ax2D.set_aspect('equal')
ax2D.set_xlim(0, 1)
ax2D.set_ylim(0, 1)
ax2D.set_title('2D Charge Density Distribution')
plt.show()

fig3D_density = plt.figure(figsize=(8, 6))
ax3D = fig3D_density.add_subplot(111, projection='3d')
density_surf = ax3D.plot_surface(X, Y, p, cmap='viridis') #, rcount=N, ccount=N, linewidth=0, antialiased=False)
fig3D_density.colorbar(density_surf, ax=ax3D, shrink=0.5, pad=0.1)
ax3D.set_xlabel('X-axis')
ax3D.set_ylabel('Y-axis')
ax3D.set_zlabel('Charge Density (rho)')
ax3D.set_title('3D Charge Density Surface')
plt.show()

fig2D_potential = plt.figure(figsize=(8, 6))
ax2D = fig2D_potential.add_subplot(111)
image = ax2D.imshow(
    V,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='jet',
    interpolation='bicubic', # 'nearest' for exact grid values, 'bicubic' for smooth visualization
    vmin=V.min(),
    vmax=V.max()
)
fig2D_potential.colorbar(image, ax=ax2D)
ax2D.set_xlabel('X-axis')
ax2D.set_ylabel('Y-axis')
ax2D.set_aspect('equal')
ax2D.set_xlim(0, 1)
ax2D.set_ylim(0, 1)
ax2D.set_title('2D Potential Distribution')
plt.show()

fig3D_potential = plt.figure(figsize=(8, 6))
ax3D = fig3D_potential.add_subplot(111, projection='3d')
surf = ax3D.plot_surface(X, Y, V, cmap='jet') #, rcount=N, ccount=N, linewidth=0, antialiased=False)
fig3D_potential.colorbar(surf, ax=ax3D, shrink=0.5, pad=0.1)
ax3D.set_xlabel('X-axis')
ax3D.set_ylabel('Y-axis')
ax3D.set_zlabel('Potential (V)')
ax3D.set_title('3D Potential Surface')
plt.show()

# 1D line curves along one side of the grid (bottom edge, index 0)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(y, p[:, 0], 'b-', linewidth=2)
ax1.set_title('Charge Density Profile along 1 side')
ax1.set_xlabel('Position (y)')
ax1.set_ylabel('Density (p)')
ax1.grid(True)

ax2.plot(y, V[:, 0], 'r-', linewidth=2)
ax2.set_title('Potential Profile along 1 side')
ax2.set_xlabel('Position (y)')
ax2.set_ylabel('Potential (V)')
ax2.grid(True)

plt.tight_layout()
plt.show()