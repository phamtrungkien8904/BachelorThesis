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


N = 101

x = np.linspace(0, 1, N)
y = np.linspace(0, 1, N)
X, Y = np.meshgrid(x, y)


rho = np.zeros((N, N))
V = np.zeros((N, N))

contact_size = 0.2
contact_width = int(contact_size * N)
V[:contact_width, :contact_width] = 1.0 # Set a square at one corner to fixed potential 10
V[-contact_width:, :contact_width] = -1.0 # Set a square at the opposite corner to fixed potential 10



def compute_potential(V, rho, max_iter=10000):
    dx = x[1] - x[0]
    fixed_mask = (V != 0)
    original_V = V.copy()
    
    for _ in range(max_iter):
        # Update using nearest neighbors (Jacobi method)
        V[1:-1, 1:-1] = 0.25 * (
            V[2:, 1:-1] + V[:-2, 1:-1] + 
            V[1:-1, 2:] + V[1:-1, :-2] + 
            rho[1:-1, 1:-1] * dx**2 
        )

        V[0, :] = V[1, :]
        V[-1, :] = V[-2, :]
        V[:, 0] = V[:, 1]
        V[:, -1] = V[:, -2]
        
        # Enforce fixed potential for contacts
        V[fixed_mask] = original_V[fixed_mask]
        
    return V

V = compute_potential(V, rho)

end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds.")

fig2D_density = plt.figure(figsize=(8, 6))
ax2D = fig2D_density.add_subplot(111)
density_image = ax2D.imshow(
    rho,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='viridis',
    interpolation='nearest', # 'nearest' for exact grid values, 'bicubic' for smooth visualization
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
density_surf = ax3D.plot_surface(X, Y, rho, cmap='viridis', rcount=N, ccount=N, linewidth=0, antialiased=False)
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
surf = ax3D.plot_surface(X, Y, V, cmap='jet', rcount=N, ccount=N, linewidth=0, antialiased=False)
fig3D_potential.colorbar(surf, ax=ax3D, shrink=0.5, pad=0.1)
ax3D.set_xlabel('X-axis')
ax3D.set_ylabel('Y-axis')
ax3D.set_zlabel('Potential (V)')
ax3D.set_title('3D Potential Surface')
plt.show()

