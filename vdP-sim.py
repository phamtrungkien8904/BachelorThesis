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
V_plus = 1.0
V_minus = -1.0

potential_vdp = np.zeros((n, n))
fixed_vdp = np.zeros((n, n), dtype=bool)

# Top-left contact at +V, bottom-left contact at -V (same side)
potential_vdp[:contact_size, :contact_size] = V_plus
potential_vdp[-contact_size:, :contact_size] = V_minus
fixed_vdp[:contact_size, :contact_size] = True
fixed_vdp[-contact_size:, :contact_size] = True

# Relax the solution while preserving corner contacts
potential_vdp = compute_potential(potential_vdp, fixed_vdp, n_iter=n_iter)

# Plot the potential distribution
fig, ax = plt.subplots(figsize=(10, 8))

# Filled contour for background
levels_filled = np.linspace(V_minus, V_plus, n)
# norm = mpl.colors.TwoSlopeNorm(vmin=V_minus, vcenter=0, vmax=V_plus)
contours = ax.contourf(xv, yv, potential_vdp, levels=levels_filled, cmap='jet')

# Extract potential at the 4 corners
V_top_left = potential_vdp[0, 0]
V_top_right = potential_vdp[0, -1]
V_bottom_left = potential_vdp[-1, 0]
V_bottom_right = potential_vdp[-1, -1]

end_time = time.time()

print(f"Execution time: {end_time - start_time:.2f} seconds")
print(f"Contact fraction: {contact_frac:.2f}")
print(f"Grid size: {n}x{n}")
print(f"Iterations: {n_iter}")
print("--- Corner Potentials ---")
print(f"Top-left (Drain):     V = {V_top_left:.4f} V0")
print(f"Bottom-left (Source):  V = {V_bottom_left:.4f} V0")
print(f"Top-right (Measured):  V = {V_top_right:.4f} V0")
print(f"Bottom-right (Measured): V = {V_bottom_right:.4f} V0")


ax.set_xlabel('x-Position (a.u.)')
ax.set_ylabel('y-Position (a.u.)')
ax.set_title("Van der Pauw's Method simulation")
fig.colorbar(contours, label='Potential V/V0')
ax.set_aspect('equal')
plt.tight_layout()
plt.show()


