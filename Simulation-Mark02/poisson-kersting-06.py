import time
import numpy as np
import matplotlib.pyplot as plt
import os

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

File_index = "04"

# Test
start_time = time.time()


kB = 1.380649e-23  # Boltzmann constant in J/K
T = 300
e = 1.602176634e-19  # Elementary charge in Coulombs
beta = 1 / (kB * T)
VT = kB * T / e

p0 = 1e18
V_bi = 2.0 * VT 
alpha = 0.005

print(f"Calculated built-in potential (V_bi): {V_bi:.4f} V")
print(f"Thermal voltage (VT): {VT:.4f} V")

epsilon = 3 * 8.854187817e-12  # Permittivity of semiconductor (epsilon_r * epsilon_0) in F/m


N = 101
iter = 100000 # Kerting's original code uses 1000 iterations, but you can increase this for better convergence at the cost of longer runtime. (Best: 2000000)
step_iter = iter//10
L = 50e-9  # Physical size of the domain in meters
x = np.linspace(0, L, N)
y = np.linspace(0, L, N)
X, Y = np.meshgrid(x, y)


V = np.zeros((N, N))
rho = np.zeros((N, N))
p = np.zeros((N, N))
contact_mask = np.zeros((N, N), dtype=bool)
cross_mask = np.zeros((N, N), dtype=bool)



contact_size = 0.05
contact_width = int(contact_size * N)
V[:contact_width, :contact_width] = V_bi + 0.0
V[-contact_width:, :contact_width] = V_bi - 0.0
contact_mask[:contact_width, :contact_width] = True
contact_mask[-contact_width:, :contact_width] = True

# Cross-shaped neutral region in the center of the domain
cross_width = 0.05
cw = int(cross_width * N)
half_cw = cw // 2
center = N // 2

# Vertical arm
cross_mask[:, center - half_cw:center + half_cw + 1] = True


# Horizontal arm
cross_mask[center - half_cw:center + half_cw + 1, :] = True

def solve():
    global V, rho, p

    dx = x[1] - x[0]

    contact_V = V.copy()



    alpha = 0.05
    error = np.zeros(iter)

    for i in range(iter):
        p = p0 *np.exp(-beta *e * (V-V_bi))
        # Neutral-background charge density
        rho = e * (p - p0)

        V_new = V.copy()

        # No semiconductor charge inside metal contacts
        p[contact_mask] = 0.0
        rho[contact_mask] = 0.0

        # No semiconductor charge in the cross region
        p[cross_mask] = 0.0
        rho[cross_mask] = 0.0

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

    return V, rho, p, error

V, rho, p, error = solve()
V = V - V_bi
p = p + p0

end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds.")

# np.savetxt(f"./Data/Data_Poti_{File_index}.dat", V)
# np.savetxt(f"./Data/Data_n2D_{File_index}.dat", p)
# np.savetxt(f"./Data/Data_Error_{File_index}.dat", error[::step_iter])

# log_filename = f"Log_{File_index}.txt"
# python_filename = os.path.basename(__file__)
# current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# # Export data to log file (txt)
# log_file = open(f"./Data/{log_filename}", 'w')
# with log_file:
#     log_file.write(f"Simulation of van der Pauw structure\n")
#     log_file.write("-------------------------------------------\n")
#     log_file.write(f"Log file for {python_filename}\n")
#     log_file.write(f"Date and time: {current_time}\n")
#     log_file.write("-------------------------------------------\n")
#     log_file.write(f"Execution time: {end_time - start_time:.2f} seconds.\n")
#     log_file.write(f"Calculated built-in potential (V_bi): {V_bi:.4f} V\n")
#     log_file.write(f"Thermal voltage (VT): {VT:.4f} V\n")
#     log_file.write(f"Number of iterations: {iter}\n")
#     log_file.write(f"Grid size: {N} x {N} ({L*1e9:.0f} nm x {L*1e9:.0f} nm)\n")



fig_density = plt.figure(figsize=(14, 6), constrained_layout=True)
gs_density = fig_density.add_gridspec(1, 2, width_ratios=[1, 1.05])

ax2D_density = fig_density.add_subplot(gs_density[0, 0])
density_image = ax2D_density.imshow(
    p,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='viridis',
    interpolation='bicubic',  # 'nearest' for exact grid values, 'bicubic' for smooth visualization
    vmin=p.min(),
    vmax=p.max()
)
fig_density.colorbar(density_image, ax=ax2D_density, shrink=0.9)
ax2D_density.set_xlabel('X-Position [nm]')
ax2D_density.set_ylabel('Y-Position [nm]')
ax2D_density.set_aspect('equal')
ax2D_density.set_xlim(0, L)
ax2D_density.set_ylim(0, L)
ax2D_density.set_title('2D Charge Density Distribution')

ax3D_density = fig_density.add_subplot(gs_density[0, 1], projection='3d')
ax3D_density.view_init(elev=30, azim=135)  # Adjust the viewing angle for better visualization
density_surf = ax3D_density.plot_surface(X, Y, p, cmap='viridis', rcount=N//3, ccount=N//3, linewidth=1, color='k', antialiased=True)
fig_density.colorbar(density_surf, ax=ax3D_density, shrink=0.6, pad=0.08)
ax3D_density.set_xlabel('X-Position [nm]')
ax3D_density.set_ylabel('Y-Position [nm]')
ax3D_density.set_zlabel('Charge Density (rho)')
ax3D_density.set_title('3D Charge Density Surface')
fig_density.suptitle('Charge Density Distribution')
plt.show()

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

# 1D line curves along one side of the grid (bottom edge, index 0)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(y, p[:, 0], 'b-', linewidth=2)
ax1.set_title('Charge Density Profile along 1 side')
ax1.set_xlabel('Position (y) [nm]')
ax1.set_ylabel('Density (p)')

ax2.plot(y, V[:, 0], 'r-', linewidth=2)
ax2.set_title('Potential Profile along 1 side')
ax2.set_xlabel('Position (y) [nm]')
ax2.set_ylabel('Potential (V)')

plt.tight_layout()
plt.show()
