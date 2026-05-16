import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1 import make_axes_locatable

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

# Constants
k_B = 1 
T = 1
beta = 1/(k_B * T)  
E_T = 1/beta  # Thermal energy

E_g = 1.0*E_T  # Band gap energy
E_F = 10  # Fermi energy at mid-gap


# Fermi-Dirac distribution function
E = np.linspace(5, 15, 400)  # Energy range
X = np.linspace(0, 1, len(E))  # Normalized x range for visualization
X_grid, E_grid = np.meshgrid(X, E)

material_ranges = [
    (0.1, 0.2),
    (0.4, 0.5),
    (0.7, 0.8),
]
material_E_V_values = [9.1, 9.5, 9.9]

f = 1 / (np.exp(beta * (E_grid - E_F)) + 1)  # Fermi-Dirac distribution

# Plot the potential distribution
fig, (ax, ax_fd) = plt.subplots(
    1,
    2,
    figsize=(12, 6),
    gridspec_kw={'width_ratios': [3, 2]},
    sharey=True,
)

# Smooth visualization for the computed grid (does not modify simulation values)
images = []

for (x_start, x_end), material_E_V in zip(material_ranges, material_E_V_values):
    x_mask = (X >= x_start) & (X <= x_end)
    material_E_C = material_E_V + E_g
    material_f = np.array(f, copy=True)
    material_f[(E_grid > material_E_V) & (E_grid < material_E_C)] = 0.0

    image = ax.imshow(
        material_f[:, x_mask],
        extent=[X[x_mask].min(), X[x_mask].max(), E.min(), E.max()],
        origin='lower',
        cmap='binary',
        alpha=0.9,
        interpolation='bicubic', # 'nearest' for exact grid values, 'bicubic' for smooth visualization
        aspect='auto',
        vmin=0,
        vmax=1
    )

    valence_border = Rectangle(
        (X[x_mask].min(), E.min()),
        X[x_mask].max() - X[x_mask].min(),
        material_E_V - E.min(),
        fill=False,
        edgecolor='black',
        linewidth=2,
        zorder=3,
    )
    ax.add_patch(valence_border)

    conduction_border = Rectangle(
        (X[x_mask].min(), material_E_C),
        X[x_mask].max() - X[x_mask].min(),
        E.max() - material_E_C,
        fill=False,
        edgecolor='black',
        linewidth=2,
        zorder=3,
    )
    ax.add_patch(conduction_border)

    images.append(image)

ax.axhline(E_F, color='k', linestyle='--', label='Fermi Energy (E_F)')
ax.axhline(E_F + k_B*T, color='k', linestyle='--')
ax.axhline(E_F - k_B*T, color='k', linestyle='--')
ax.set_title('Band Diagram')
ax.set_xlabel('')
ax.set_ylabel('Energy (E)')
ax.set_yticks([E_F, E_F + k_B*T, E_F - k_B*T])
ax.set_yticklabels([r'$E_F$', r'$E_F + k_B T$', r'$E_F - k_B T$'])
ax.set_xlim(X.min(), X.max())
ax.set_ylim(E.min(), E.max())
ax.set_xticks([])

f_fd = 1 / (np.exp(beta * (E - E_F)) + 1)
ax_fd.plot(f_fd, E, color='blue', lw=2, label='Fermi-Dirac distribution')
ax_fd.axhline(E_F, color='k', linestyle='--', linewidth=1)
ax_fd.axhline(E_F + k_B*T, color='k', linestyle='--', linewidth=1)
ax_fd.axhline(E_F - k_B*T, color='k', linestyle='--', linewidth=1)
ax_fd.set_title('Fermi-Dirac Distribution')
ax_fd.set_xlabel('f(E)')
ax_fd.set_xlim(0, 1)
ax_fd.tick_params(axis='y', left=False, labelleft=False)


cbar_axis = make_axes_locatable(ax_fd).append_axes("right", size="10%", pad=0.5)
cbar = fig.colorbar(images[0], cax=cbar_axis)
cbar.set_label('Electron probability')

plt.show()

