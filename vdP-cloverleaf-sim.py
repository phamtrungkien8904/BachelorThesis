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

# Four closed rectangular cloverleaf regions fixed at 0 potential:
# 1) (-1.0, 0.1) -> (-0.2, 0.1) -> (-0.2, -0.1) -> (-1.0, -0.1)
# 2) ( 1.0, 0.1) -> ( 0.2, 0.1) -> ( 0.2, -0.1) -> ( 1.0, -0.1)
# 3) ( 0.1, 1.0) -> ( 0.1, 0.2) -> (-0.1, 0.2) -> (-0.1, 1.0)
# 4) ( 0.1,-1.0) -> ( 0.1,-0.2) -> (-0.1,-0.2) -> (-0.1,-1.0)

# Keep two driving contacts from the original setup.
contact_frac = 0.4
contact_size = int(contact_frac * n)
V_plus = 1.0
V_minus = -1.0


potential_vdp = np.zeros((n, n))
fixed_vdp = np.zeros((n, n), dtype=bool)

# Build masks for the four rectangles on the simulation grid.
rec_size = np.array([0.8, 0.1])  # [arm_length_from_edge, arm_thickness]
rec_len, rec_thickness = rec_size

if not (0 < rec_len <= 2.0 and 0 < rec_thickness <= 2.0):
    raise ValueError("rec_size must satisfy 0 < rec_len, rec_thickness <= 2.0")

half_thickness = rec_thickness / 2.0

left_rect = (xv >= -1.0) & (xv <= -1.0 + rec_len) & (yv >= -half_thickness) & (yv <= half_thickness)
right_rect = (xv >= 1.0 - rec_len) & (xv <= 1.0) & (yv >= -half_thickness) & (yv <= half_thickness)
top_rect = (xv >= -half_thickness) & (xv <= half_thickness) & (yv >= 1.0 - rec_len) & (yv <= 1.0)
bottom_rect = (xv >= -half_thickness) & (xv <= half_thickness) & (yv >= -1.0) & (yv <= -1.0 + rec_len)

cloverleaf_mask = left_rect | right_rect | top_rect | bottom_rect
potential_vdp[cloverleaf_mask] = 0.0
fixed_vdp[cloverleaf_mask] = True

# Driving contacts (top-left at +V, bottom-left at -V).
plus_contact = np.zeros((n, n), dtype=bool)
minus_contact = np.zeros((n, n), dtype=bool)
plus_contact[:contact_size, :contact_size] = True
minus_contact[-contact_size:, :contact_size] = True

potential_vdp[plus_contact] = V_plus
potential_vdp[minus_contact] = V_minus
fixed_vdp[plus_contact] = True
fixed_vdp[minus_contact] = True

# Relax the solution while preserving fixed contacts
potential_vdp = compute_potential(potential_vdp, fixed_vdp, n_iter=n_iter)



# Plot the potential distribution
fig, ax = plt.subplots(figsize=(10, 8))

# Filled contour for background
vmax = np.max(np.abs(potential_vdp))
if vmax < 1e-9:
    vmax = 1.0
levels_filled = np.linspace(-vmax, vmax, n)
contours = ax.contourf(xv, yv, potential_vdp, levels=levels_filled, cmap='jet')
ax.contour(xv, yv, cloverleaf_mask.astype(float), levels=[0.5], colors='black', linewidths=1.2)


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