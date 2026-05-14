import numpy as np
import matplotlib.pyplot as plt

File_index = "02"

data_Poti = np.loadtxt(f"./Data/Data_Poti_{File_index}.dat")
data_n2D = np.loadtxt(f"./Data/Data_n2D_{File_index}.dat")
data_error = np.loadtxt(f"./Data/Data_Error_{File_index}.dat")
error_index = np.arange(1, len(data_error) + 1)

N = 101
L = 50  # Physical size of the domain in nm
x = np.linspace(0, L, N)
y = np.linspace(0, L, N)
X, Y = np.meshgrid(x, y)

V = data_Poti
p = data_n2D


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


plt.plot(error_index, data_error)
plt.yscale("log")
plt.xlabel("Iteration")
plt.ylabel("Error (log scale)")
plt.title("Convergence of Poisson Solver")
plt.grid()
plt.show()
