import os
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


File_index = "01"
# Test
start_time = time.time()


# kB = 1.380649e-23  # Boltzmann constant in J/K
# T = 300
# e = 1.602176634e-19  # Elementary charge in Coulombs
# beta = 1 / (kB * T)
# VT = kB * T / e

# p0 = 1e18
# V_bi = 2.0 * VT 
# alpha = 0.005

# print(f"Calculated built-in potential (V_bi): {V_bi:.4f} V")
# print(f"Thermal voltage (VT): {VT:.4f} V")

epsilon = 1  # Permittivity of semiconductor (epsilon_r * epsilon_0) in F/m


N = 101
iter = 2000000 # Kerting's original code uses 1000 iterations, but you can increase this for better convergence at the cost of longer runtime. (Best: 2000000)
step_iter = 100000
L = 50e-9  # Physical size of the domain in meters
x = np.linspace(0, L, N)
y = np.linspace(0, L, N)
X, Y = np.meshgrid(x, y)


V = np.zeros((N, N))
rho = np.zeros((N, N))
contact_mask = np.zeros((N, N), dtype=bool)



contact_size = 0.1
contact_radius = max(int(contact_size * N), 1)
rows, cols = np.ogrid[:N, :N]
top_contact_mask = rows**2 + cols**2 <= contact_radius**2
bottom_contact_mask = (rows - (N - 1))**2 + cols**2 <= contact_radius**2
contact_mask = top_contact_mask | bottom_contact_mask
V[top_contact_mask] = 1.0
V[bottom_contact_mask] = -1.0




def solve():
    global V

    dx = x[1] - x[0]

    contact_V = V.copy()

    alpha = 0.05
    error = np.zeros(iter)

    for i in range(iter):
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
        error[i] = 100.0 * np.max(np.abs(V_new - V)) / max(np.max(np.abs(V)), 1e-30)
        V = (1 - alpha) * V + alpha * V_new

        if (i + 1) % step_iter == 0:
            print(f"Iteration: {i + 1}/{iter}, Error: {error[i]:.6e} %")

    return V

V= solve()


end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds.")

dx = x[1] - x[0]
dV_dy, dV_dx = np.gradient(V, dx, dx)
Ex = -dV_dx
Ey = -dV_dy
E_mag = np.sqrt(Ex**2 + Ey**2)

# For quiver plot
s = 5
X_q = X[::s, ::s]
Y_q = Y[::s, ::s]
Ex_q = Ex[::s, ::s]
Ey_q = Ey[::s, ::s]
E_mag_q = np.hypot(Ex_q, Ey_q)


quiver_scale = np.nanmax(E_mag_q) / (0.4 * dx) if np.nanmax(E_mag_q) > 0 else 1.0



fig_potential = plt.figure(figsize=(14, 6), constrained_layout=True)
gs_potential = fig_potential.add_gridspec(1, 2, width_ratios=[1, 1.05])

ax2D_potential = fig_potential.add_subplot(gs_potential[0, 0])
image = ax2D_potential.imshow(
    V,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='jet',
    interpolation='bicubic',  # 'nearest' for exact grid values, 'bicubic' for smooth visualization
    vmin=V.min(),
    vmax=V.max()
)
plt.rcParams['contour.negative_linestyle'] = 'solid'
contour = ax2D_potential.contour(X, Y, V, colors='k', levels=30, linewidths=1)

fig_potential.colorbar(image, ax=ax2D_potential, shrink=0.9)
ax2D_potential.set_xlabel('X-Position [nm]')
ax2D_potential.set_ylabel('Y-Position [nm]')
ax2D_potential.set_aspect('equal')
ax2D_potential.set_xlim(0, L)
ax2D_potential.set_ylim(0, L)
ax2D_potential.set_title('2D Potential Distribution')

ax3D_potential = fig_potential.add_subplot(gs_potential[0, 1], projection='3d')
ax3D_potential.view_init(elev=30, azim=135)  # Adjust the viewing angle for better visualization
surf = ax3D_potential.plot_surface(X, Y, V, cmap='jet', rcount=N//3, ccount=N//3, linewidth=1, color='k', antialiased=True)
fig_potential.colorbar(surf, ax=ax3D_potential, shrink=0.6, pad=0.08)
ax3D_potential.set_xlabel('X-Position [nm]')
ax3D_potential.set_ylabel('Y-Position [nm]')
ax3D_potential.set_zlabel('Potential (V)')
ax3D_potential.set_title('3D Potential Surface')
fig_potential.suptitle('Potential Distribution')

plt.show()


fig_field = plt.figure(figsize=(14, 6), constrained_layout=True)
gs_field = fig_field.add_gridspec(1, 2, width_ratios=[1, 1.05])

ax2D_field = fig_field.add_subplot(gs_field[0, 0])
image = ax2D_field.imshow(
    E_mag,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='jet',
    interpolation='bicubic',  # 'nearest' for exact grid values, 'bicubic' for smooth visualization
    vmin=E_mag.min(),
    vmax=E_mag.max()
)

fig_field.colorbar(image, ax=ax2D_field, shrink=0.9)
ax2D_field.set_xlabel('X-Position [nm]')
ax2D_field.set_ylabel('Y-Position [nm]')
ax2D_field.set_aspect('equal')
ax2D_field.set_xlim(0, L)
ax2D_field.set_ylim(0, L)
ax2D_field.set_title('2D Electric Field Magnitude Distribution')

ax3D_field = fig_field.add_subplot(gs_field[0, 1], projection='3d')
ax3D_field.view_init(elev=30, azim=135)  # Adjust the viewing angle for better visualization
surf = ax3D_field.plot_surface(X, Y, E_mag, cmap='jet', rcount=N//3, ccount=N//3, linewidth=1, color='k', antialiased=True)
fig_field.colorbar(surf, ax=ax3D_field, shrink=0.6, pad=0.08)
ax3D_field.set_xlabel('X-Position [nm]')
ax3D_field.set_ylabel('Y-Position [nm]')
ax3D_field.set_zlabel('Electric Field Magnitude (V/m)')
ax3D_field.set_title('3D Electric Field Magnitude Surface')
fig_field.suptitle('Electric Field Distribution')

plt.show()


fig_field, ax_field = plt.subplots(figsize=(7, 6), constrained_layout=True)
quiver = ax_field.quiver(
    X_q,
    Y_q,
    Ex_q,
    Ey_q,
    color='black',
    angles='xy',
    scale_units='xy',
    scale=quiver_scale*0.05,
    pivot='mid',
)
# fig_field.colorbar(quiver, ax=ax_field, label='|E| [V/m]')
ax_field.set_xlabel('X-Position [nm]')
ax_field.set_ylabel('Y-Position [nm]')
ax_field.set_aspect('equal')
ax_field.set_xlim(0, L)
ax_field.set_ylim(0, L)
ax_field.set_title('Electric Field Quiver')
plt.show()

# 1D line curves along one side of the grid (bottom edge, index 0)
fig = plt.figure(figsize=(8, 6))
ax2 = fig.add_subplot(111)
ax2.plot(y, V[:, 0], 'r-', linewidth=2)
ax2.set_title('Potential Profile along 1 side')
ax2.set_xlabel('Position (y) [nm]')
ax2.set_ylabel('Potential (V)')

plt.tight_layout()
plt.show()

