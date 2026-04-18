import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time

# Custom settings
plt.style.use('classic')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['mathtext.fontset'] = 'dejavusans'
plt.rcParams['figure.dpi'] = 100

start_time = time.time()
n = 100
n_iter = 1000
edge = np.linspace(-1, 1, n)
upper_y = np.cos(np.pi * edge / 2)
lower_y = edge**4
upper_x = 1/(np.e**-1 - np.e) * (np.exp(edge)-np.e)
lower_x = 0.5 * (edge**2-edge)
xv, yv = np.meshgrid(edge, edge)

def compute_potential(potential, fixed_bool, n_iter):
    length = len(potential[0])
    for n in range(n_iter):
        for i in range(1, length-1):
            for j in range(1, length-1):
                if not(fixed_bool[j][i]):
                    potential[j][i] = 1/4 * (potential[j+1][i] + potential[j-1][i] + potential[j][i+1] + potential[j][i-1])
    return potential

# Van der Pauw corner voltage simulation

contact_frac = 0.2
contact_size = int(contact_frac * n)
contact_radius = 2.0 * contact_frac
V_plus = 1.0
V_minus = -1.0

potential_vdp = np.zeros((n, n))
fixed_vdp = np.zeros((n, n), dtype=bool)

# Quarter-circle contacts centered at the left corners.
top_left_contact = (
    ((xv + 1.0) ** 2 + (yv - 1.0) ** 2 <= contact_radius ** 2)
    & (xv <= -1.0 + contact_radius)
    & (yv >= 1.0 - contact_radius)
)
bottom_left_contact = (
    ((xv + 1.0) ** 2 + (yv + 1.0) ** 2 <= contact_radius ** 2)
    & (xv <= -1.0 + contact_radius)
    & (yv <= -1.0 + contact_radius)
)

potential_vdp[top_left_contact] = V_plus
potential_vdp[bottom_left_contact] = V_minus
fixed_vdp[top_left_contact] = True
fixed_vdp[bottom_left_contact] = True

# Relax the solution while preserving corner contacts
potential_vdp = compute_potential(potential_vdp, fixed_vdp, n_iter=n_iter)



# Plot the potential distribution
fig, ax = plt.subplots(figsize=(10, 8))

# Filled contour for background
levels_filled = np.linspace(V_minus, V_plus, n)
# norm = mpl.colors.TwoSlopeNorm(vmin=V_minus, vcenter=0, vmax=V_plus)
contours = ax.contourf(xv, yv, potential_vdp, levels=levels_filled, cmap='jet')

# # Equipotential lines with 0.1 V_0 spacing
# equipotential_levels = np.arange(V_minus, V_plus + 0.1, 0.1)
# contour_lines = ax.contour(xv, yv, potential_vdp, levels=equipotential_levels, colors='black', linewidths=0.5, alpha=0.4)
# ax.clabel(contour_lines, inline=True, fontsize=8, fmt='%.1f')

# # Compute electric field E = -∇V
# dy, dx = np.gradient(-potential_vdp)

# # Downsample for cleaner quiver plot
# skip = max(1, n // 15)  # Show ~15x15 arrows
# Ex_sparse = dx[::skip, ::skip]
# Ey_sparse = dy[::skip, ::skip]
# xv_sparse = xv[::skip, ::skip]
# yv_sparse = yv[::skip, ::skip]

# # Normalize arrows for visual clarity
# magnitude = np.sqrt(Ex_sparse**2 + Ey_sparse**2)
# magnitude[magnitude == 0] = 1
# Ex_norm = Ex_sparse / magnitude
# Ey_norm = Ey_sparse / magnitude

# # Plot electric field
# quiv = ax.quiver(xv_sparse, yv_sparse, Ex_norm, Ey_norm, magnitude, cmap='cool', scale=30, width=0.003)
# ax.quiverkey(quiv, X=0.9, Y=1.05, U=1, label='E-field', labelpos='E')

end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")
print(f"Contact fraction: {contact_frac:.2f}")
print(f"Grid size: {n}x{n}")
print(f"Iterations: {n_iter}")

ax.set_xlabel('x-Position (a.u.)')
ax.set_ylabel('y-Position (a.u.)')
ax.set_title("Van der Pauw's Method simulation")
fig.colorbar(contours, label='Potential V/V0')
ax.set_aspect('equal')
plt.tight_layout()
plt.show()