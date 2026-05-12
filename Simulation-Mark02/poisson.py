import time
import numpy as np
import matplotlib.pyplot as plt
from pandas import NA

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
beta = 1
e = 1
Nv = 1.0  # Scaled down to prevent divergence
E_F = 1.0
Ev0 = 0.9
EA0 = 1.0
gA = 4
epsilon = 1


N = 101
iter = 10000

x = np.linspace(0, 1, N)
y = np.linspace(0, 1, N)
X, Y = np.meshgrid(x, y)


V = np.zeros((N, N))
rho = np.zeros((N, N))
contact_mask = np.zeros((N, N), dtype=bool)



contact_size = 0.1
contact_width = int(contact_size * N)
V[:contact_width, :contact_width] = 0.0
V[-contact_width:, :contact_width] = 0.0
rho[:contact_width, :contact_width] = 0.0
rho[-contact_width:, :contact_width] = 0.0
contact_mask[:contact_width, :contact_width] = True
contact_mask[-contact_width:, :contact_width] = True




def solve():
    global V, rho

    dx = x[1] - x[0]

    contact_V = V.copy()


    alpha = 0.05

    for _ in range(iter):

        # Valence band / HOMO energy
        Ev = Ev0 - e * V

        # Hole density from Fermi-Dirac
        p = Nv *(1 + np.exp(np.clip(beta * (E_F - Ev), -100, 100)))
        
        EA = EA0 - e * V
        NA_minus = NA / (1 + gA * np.exp(np.clip((EA - E_F)*beta, -100, 100)))

        # Neutral-background charge density
        rho = e * (p - NA_minus)

        # No semiconductor charge inside metal contacts
        rho[contact_mask] = 0.0

        # Poisson update
        V_new = V.copy()

        V_new[1:-1, 1:-1] = 0.25 * (
            V[2:, 1:-1]
            + V[:-2, 1:-1]
            + V[1:-1, 2:]
            + V[1:-1, :-2]
            + dx**2 * rho[1:-1, 1:-1] / epsilon
        )

        # Neumann outer boundaries: dV/dn = 0
        V_new[0, :] = V_new[1, :]
        V_new[-1, :] = V_new[-2, :]
        V_new[:, 0] = V_new[:, 1]
        V_new[:, -1] = V_new[:, -2]

        # Dirichlet contacts
        V_new[contact_mask] = contact_V[contact_mask]

        # Relaxation
        V = (1 - alpha) * V + alpha * V_new

    return V, rho

V, rho = solve()

end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds.")

fig2D_density = plt.figure(figsize=(8, 6))
ax2D = fig2D_density.add_subplot(111)
density_image = ax2D.imshow(
    rho,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='viridis',
    interpolation='bicubic', # 'nearest' for exact grid values, 'bicubic' for smooth visualization
    vmin=rho.min(),
    vmax=rho.max()
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
density_surf = ax3D.plot_surface(X, Y, rho, cmap='viridis') #, rcount=N, ccount=N, linewidth=0, antialiased=False)
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

