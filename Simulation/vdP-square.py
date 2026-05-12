import numpy as np
import matplotlib.pyplot as plt
import time
import os
from datetime import date
from mpl_toolkits.mplot3d import Axes3D

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

# Simulation parameters (Defaults: n=100, n_iter=1000 for quick testing; n=1000 (10s), n_iter=10000 for higher accuracy (2 hours))
n = 100
n_iter = 1000
edge = np.linspace(-1, 1, n)
xv, yv = np.meshgrid(edge, edge)
grid_spacing = edge[1] - edge[0]

# Homogeneous charge density for the Poisson equation test case.
charge_density_value = 16.0
charge_density = np.full((n, n), charge_density_value)

# # Gaussian charge defect in the middle of the grid
# defect_amplitude = 50.0
# defect_sigma = 0.1
# charge_density += defect_amplitude * np.exp(-(xv**2 + yv**2) / (2 * defect_sigma**2))

epsilon_0 = 1.0

def compute_potential(potential, fixed_bool, charge_density, n_iter):
    length = len(potential[0])
    for n in range(n_iter):
        for i in range(1, length-1):
            for j in range(1, length-1):
                if not(fixed_bool[j][i]):
                    potential[j][i] = 1/4 * (
                        potential[j+1][i]
                        + potential[j-1][i]
                        + potential[j][i+1]
                        + potential[j][i-1]
                        + (grid_spacing ** 2) * charge_density[j][i] / epsilon_0
                    )

        # Keep the outer boundary free to float by mirroring the nearest interior values.
        potential[0, :] = potential[1, :]
        potential[-1, :] = potential[-2, :]
        potential[:, 0] = potential[:, 1]
        potential[:, -1] = potential[:, -2]

        # Restore fixed contact values after updating the boundary.
        potential[fixed_bool] = potential_vdp[fixed_bool]
    return potential

# Van der Pauw corner voltage simulation

contact_frac = 0.1
contact_size = int(contact_frac * n)
V_plus = 5.0
V_minus = 0.0

potential_vdp = np.zeros((n, n))
fixed_vdp = np.zeros((n, n), dtype=bool)

# Top-left contact at +V, bottom-left contact at -V (same side)
potential_vdp[:contact_size, :contact_size] = V_plus
potential_vdp[-contact_size:, :contact_size] = V_minus
fixed_vdp[:contact_size, :contact_size] = True
fixed_vdp[-contact_size:, :contact_size] = True

# Schottky contacts have no charge density
charge_density[fixed_vdp] = 0.0

# Relax the solution while preserving corner contacts
potential_vdp = compute_potential(potential_vdp, fixed_vdp, charge_density, n_iter=n_iter)

# Plot the potential distribution
fig, ax = plt.subplots(figsize=(8, 6))

# # Filled contour for background
# levels_filled = np.linspace(V_minus, V_plus, n_iter)
# # norm = mpl.colors.TwoSlopeNorm(vmin=V_minus, vcenter=0, vmax=V_plus)
# image = ax.contourf(xv, yv, potential_vdp, levels=levels_filled, cmap='jet')

# Smooth visualization for the computed grid (does not modify simulation values)
image = ax.imshow(
    potential_vdp,
    extent=[edge.min(), edge.max(), edge.min(), edge.max()],
    origin='lower',
    cmap='jet',
    interpolation='bicubic', # 'nearest' for exact grid values, 'bicubic' for smooth visualization
    vmin=V_minus,
    vmax=V_plus
)



# Extract potential at the 4 corners
V_bottom_left = potential_vdp[0, 0]
V_bottom_right = potential_vdp[0, -1]
V_top_left = potential_vdp[-1, 0]
V_top_right = potential_vdp[-1, -1]

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
potential_fraction = (V_top_right - V_bottom_right) / (V_minus - V_plus)
print(f"Potential fraction: V21/V34 = {potential_fraction:.4f}")

log_index = "20261105001"
log_filename = "vdP_log_" + log_index + ".txt"
python_filename = os.path.basename(__file__)
today_str = date.today().isoformat()

left_info = (
    f"Log file: {log_filename}\n"
    f"Python file: {python_filename}\n"
    f"Execution time: {end_time - start_time:.2f} s\n"
    f"Grid size: {n} x {n}\n"
    f"Potential steps: {n_iter}\n"
    f"Charge density: homogeneous (rho={charge_density_value:.2f})\n"
    f"Potential fraction: {potential_fraction:.4f}"
)

right_info = f"Date: {today_str}"

ax.set_xlabel('x-Position (a.u.)')
ax.set_ylabel('y-Position (a.u.)')
ax.set_title("Van der Pauw's Method simulation", pad=80)
ax.text(0.0, 1.01, left_info, transform=ax.transAxes, ha='left', va='bottom', fontsize=10)
ax.text(1.0, 1.01, right_info, transform=ax.transAxes, ha='right', va='bottom', fontsize=10)
fig.colorbar(image, label='Potential V/V0')
ax.set_aspect('equal')
plt.tight_layout()

# Save the figure as EPS
fig.savefig("vdP_eps_" + log_index + ".eps", format='eps', bbox_inches='tight')
fig.savefig("vdP_png_" + log_index + ".png", format='png', bbox_inches='tight', dpi=600)

# 3D surface plot of the potential distribution
fig3d = plt.figure(figsize=(8, 6))
ax3d = fig3d.add_subplot(111, projection='3d')
surface = ax3d.plot_surface(
    xv,
    yv,
    potential_vdp,
    cmap='jet',
    linewidth=0,
    antialiased=True,
    rcount=potential_vdp.shape[0],
    ccount=potential_vdp.shape[1],
    vmin=V_minus,
    vmax=V_plus,
)
ax3d.set_xlabel('x-Position (a.u.)')
ax3d.set_ylabel('y-Position (a.u.)')
ax3d.set_zlabel('Potential V/V0')
ax3d.set_title("Van der Pauw's Method simulation - 3D potential")
ax3d.view_init(elev=30, azim=-135)
fig3d.colorbar(surface, ax=ax3d, shrink=0.75, pad=0.1, label='Potential V/V0')
fig3d.savefig("vdP_3d_" + log_index + ".eps", format='eps', bbox_inches='tight')
fig3d.savefig("vdP_3d_" + log_index + ".png", format='png', bbox_inches='tight', dpi=600)

# 2D cross-section plot along the bottom edge (y = -1)
fig1d = plt.figure(figsize=(8, 6))
ax1d = fig1d.add_subplot(111)
ax1d.plot(edge, potential_vdp[:, 0], 'b-', linewidth=2)
ax1d.set_xlim(-1, 1)
ax1d.set_ylim(V_minus * 1.1, V_plus * 1.1)
ax1d.set_xlabel('x-Position (a.u.)')
ax1d.set_ylabel('Potential V/V0')
ax1d.set_title('Potential profile along the bottom edge')
fig1d.savefig("vdP_1d_edge_" + log_index + ".eps", format='eps', bbox_inches='tight')
fig1d.savefig("vdP_1d_edge_" + log_index + ".png", format='png', bbox_inches='tight', dpi=600)

# 2D imshow of charge density
fig_rho_2d, ax_rho_2d = plt.subplots(figsize=(8, 6))
image_rho = ax_rho_2d.imshow(
    charge_density,
    extent=[edge.min(), edge.max(), edge.min(), edge.max()],
    origin='lower',
    cmap='viridis',
    interpolation='nearest'
)
ax_rho_2d.set_xlabel('x-Position (a.u.)')
ax_rho_2d.set_ylabel('y-Position (a.u.)')
ax_rho_2d.set_title("Charge Density 2D")
fig_rho_2d.colorbar(image_rho, label='Charge density')
fig_rho_2d.savefig("vdP_rho_2d_" + log_index + ".png", format='png', bbox_inches='tight', dpi=600)

# 3D surface plot of the charge density distribution
fig_rho_3d = plt.figure(figsize=(8, 6))
ax_rho_3d = fig_rho_3d.add_subplot(111, projection='3d')
surface_rho = ax_rho_3d.plot_surface(
    xv,
    yv,
    charge_density,
    cmap='viridis',
    linewidth=0,
    antialiased=True,
    rcount=charge_density.shape[0],
    ccount=charge_density.shape[1],
)
ax_rho_3d.set_xlabel('x-Position (a.u.)')
ax_rho_3d.set_ylabel('y-Position (a.u.)')
ax_rho_3d.set_zlabel('Charge density')
ax_rho_3d.set_title("Charge Density 3D")
ax_rho_3d.view_init(elev=30, azim=-135)
fig_rho_3d.colorbar(surface_rho, ax=ax_rho_3d, shrink=0.75, pad=0.1, label='Charge density')
fig_rho_3d.savefig("vdP_rho_3d_" + log_index + ".png", format='png', bbox_inches='tight', dpi=600)

plt.show()

# Export data to log file (txt)
log_file = open("vdP_log_" + log_index + ".txt", 'w')
with log_file:
    log_file.write("Van der Pauw Simulation Log-File\n")
    log_file.write("-------------------------------\n")
    log_file.write(f"Python file:            {python_filename}\n")
    log_file.write(f"Execution time:         {end_time - start_time:.2f} seconds\n")
    log_file.write(f"Contact size fraction:  {contact_frac:.2f}\n")
    log_file.write(f"Grid size:              {n} x {n}\n")
    log_file.write(f"Potential steps:        {n_iter}\n")
    log_file.write(f"Charge density:         homogeneous (rho={charge_density_value:.2f})\n")
    log_file.write("--- Corner Potentials ---\n")
    log_file.write(f"Top-left (Drain):        V = {V_top_left:.4f} V0\n")
    log_file.write(f"Bottom-left (Source):    V = {V_bottom_left:.4f} V0\n")
    log_file.write(f"Top-right (Measured):    V = {V_top_right:.4f} V0\n")
    log_file.write(f"Bottom-right (Measured): V = {V_bottom_right:.4f} V0\n")
    log_file.write(f"Potential fraction:      V21/V34 = {potential_fraction:.4f}\n")

