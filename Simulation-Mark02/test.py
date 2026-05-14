import numpy as np
import matplotlib.pyplot as plt


data_Poti = np.loadtxt("Data_Poti_01.dat")
data_n2D = np.loadtxt("Data_n2D_01.dat")
data_error = np.loadtxt("Data_Error_01.dat")
error_index = np.arange(1, len(data_error) + 1)

N = 101
L = 50e-9  # Physical size of the domain in meters
x = np.linspace(0, L, N)
y = np.linspace(0, L, N)
X, Y = np.meshgrid(x, y)

V = data_Poti
p = data_n2D
print(p.max())

fig2D_density = plt.figure(figsize=(8, 6))
ax2D = fig2D_density.add_subplot(111)
density_image = ax2D.imshow(
    p,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='viridis',
    interpolation='bicubic', # 'nearest' for exact grid values, 'bicubic' for smooth visualization
    vmin=p.max(),
    vmax=p.min()
)
fig2D_density.colorbar(density_image, ax=ax2D)
ax2D.set_xlabel('X-axis')
ax2D.set_ylabel('Y-axis')
ax2D.set_aspect('equal')
ax2D.set_xlim(0, L)
ax2D.set_ylim(0, L)
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
ax2D.set_xlim(0, L)
ax2D.set_ylim(0, L)
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


plt.plot(error_index, data_error)
plt.yscale("log")
plt.xlabel("Iteration")
plt.ylabel("Error (log scale)")
plt.title("Convergence of Poisson Solver")
plt.grid()
plt.show()
