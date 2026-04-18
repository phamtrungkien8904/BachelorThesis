import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time

# Custom settings
plt.style.use('classic')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['figure.dpi'] = 100

start_time = time.time()
n = 100
n_iter = 1000
edge = np.linspace(-1, 1, n)
xv, yv = np.meshgrid(edge, edge)


def compute_potential(potential, fixed_bool, n_iter):
    length = len(potential[0])
    for n in range(n_iter):
        for i in range(1, length - 1):
            for j in range(1, length - 1):
                if not fixed_bool[j][i]:
                    potential[j][i] = 0.25 * (
                        potential[j + 1][i]
                        + potential[j - 1][i]
                        + potential[j][i + 1]
                        + potential[j][i - 1]
                    )
    return potential


# Cloverleaf with grounded rectangular arms + round corner contacts
rec_size = np.array([0.8, 0.1])  # [arm_length_from_edge, arm_thickness]
rec_len, rec_thickness = rec_size

if not (0 < rec_len <= 2.0 and 0 < rec_thickness <= 2.0):
    raise ValueError('rec_size must satisfy 0 < rec_len, rec_thickness <= 2.0')

contact_frac = 0.2
contact_radius = 2.0 * contact_frac
V_plus = 1.0
V_minus = -1.0

potential_vdp = np.zeros((n, n))
fixed_vdp = np.zeros((n, n), dtype=bool)

half_thickness = rec_thickness / 2.0

left_rect = (xv >= -1.0) & (xv <= -1.0 + rec_len) & (yv >= -half_thickness) & (yv <= half_thickness)
right_rect = (xv >= 1.0 - rec_len) & (xv <= 1.0) & (yv >= -half_thickness) & (yv <= half_thickness)
top_rect = (xv >= -half_thickness) & (xv <= half_thickness) & (yv >= 1.0 - rec_len) & (yv <= 1.0)
bottom_rect = (xv >= -half_thickness) & (xv <= half_thickness) & (yv >= -1.0) & (yv <= -1.0 + rec_len)

cloverleaf_mask = left_rect | right_rect | top_rect | bottom_rect
potential_vdp[cloverleaf_mask] = 0.0
fixed_vdp[cloverleaf_mask] = True

# Quarter-circle driving contacts centered at the left corners.
plus_contact = (
    ((xv + 1.0) ** 2 + (yv - 1.0) ** 2 <= contact_radius ** 2)
    & (xv <= -1.0 + contact_radius)
    & (yv >= 1.0 - contact_radius)
)
minus_contact = (
    ((xv + 1.0) ** 2 + (yv + 1.0) ** 2 <= contact_radius ** 2)
    & (xv <= -1.0 + contact_radius)
    & (yv <= -1.0 + contact_radius)
)

potential_vdp[plus_contact] = V_plus
potential_vdp[minus_contact] = V_minus
fixed_vdp[plus_contact] = True
fixed_vdp[minus_contact] = True

# Relax the solution while preserving fixed regions.
potential_vdp = compute_potential(potential_vdp, fixed_vdp, n_iter=n_iter)

# Plot the potential distribution
fig, ax = plt.subplots(figsize=(10, 8))

vmax = np.max(np.abs(potential_vdp))
if vmax < 1e-9:
    vmax = 1.0

levels_filled = np.linspace(-vmax, vmax, n)
contours = ax.contourf(xv, yv, potential_vdp, levels=levels_filled, cmap='seismic')
ax.contour(xv, yv, cloverleaf_mask.astype(float), levels=[0.5], colors='black', linewidths=1.2)
# ax.contour(xv, yv, plus_contact.astype(float), levels=[0.5], colors='gold', linewidths=1.0)
# ax.contour(xv, yv, minus_contact.astype(float), levels=[0.5], colors='gold', linewidths=1.0)

end_time = time.time()
print(f'Execution time: {end_time - start_time:.2f} seconds')
print(f'Grounded cloverleaf points: {np.count_nonzero(cloverleaf_mask)}')
print(f'Driven +V round contact points: {np.count_nonzero(plus_contact)}')
print(f'Driven -V round contact points: {np.count_nonzero(minus_contact)}')
print(f'Grid size: {n}x{n}')
print(f'Iterations: {n_iter}')

ax.set_xlabel('x-Position (a.u.)')
ax.set_ylabel('y-Position (a.u.)')
ax.set_title("Van der Pauw's Method simulation (cloverleaf + round contacts)")
fig.colorbar(contours, label='Potential V/V0')
ax.set_aspect('equal')
plt.tight_layout()
plt.show()
