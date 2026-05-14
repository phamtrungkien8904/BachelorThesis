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

V_bi = 0.5   # Built-in potential in volts (Ohmic contact)


epsilon = 1


N = 101
iter = 2000000 # Kerting's original code uses 1000 iterations, but you can increase this for better convergence at the cost of longer runtime. (Best: 2000000)
x = np.linspace(0, 1, N)
y = np.linspace(0, 1, N)
X, Y = np.meshgrid(x, y)


V = np.zeros((N, N))
rho = np.zeros((N, N))
p = np.zeros((N, N))
contact_mask = np.zeros((N, N), dtype=bool)



contact_size = 0.05
contact_width = int(contact_size * N)
V[:contact_width, :contact_width] = V_bi + 0.0
V[-contact_width:, :contact_width] = V_bi - 1.0
# rho[:contact_width, :contact_width] = 0.0
# rho[-contact_width:, :contact_width] = 0.0
# p[:contact_width, :contact_width] = 0.0
# p[-contact_width:, :contact_width] = 0.0
contact_mask[:contact_width, :contact_width] = True
contact_mask[-contact_width:, :contact_width] = True




def solve():
    global V, rho, p

    dx = x[1] - x[0]

    contact_V = V.copy()



    alpha = 0.05

    for i in range(iter):
        p0 = 10.0
        p = p0 *(np.exp(-beta *e * (V-V_bi)) - 1)
        # Neutral-background charge density
        rho = e * p

        # No semiconductor charge inside metal contacts
        p[contact_mask] = 0.0
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
        error = np.max(np.abs(V_new - V))
        V = (1 - alpha) * V + alpha * V_new

        if (i + 1) % 5000 == 0:
            print(f"Step {i + 1}/{iter}, Error: {error:.6e}")

    return V, rho, p

V, rho, p = solve()
V = V - V_bi

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