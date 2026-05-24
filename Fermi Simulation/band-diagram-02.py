import numpy as np
import matplotlib.pyplot as plt

# Custom settings
plt.style.use('classic')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['mathtext.fontset'] = 'cm'
# plt.rcParams['figure.dpi'] = 100

# Constants
k_B = 1 
T = 1
beta = 1/(k_B * T)  
E_T = 1/beta  # Thermal energy

E_g = 3.0*E_T  # Band gap energy
E_F = 10  # Fermi energy at mid-gap


# Fermi-Dirac distribution function
E = np.linspace(E_F - 10*E_T, E_F + 10*E_T, 2000)  # Energy range
X = np.linspace(-0.5, 1.5, len(E))  # Normalized x range for visualization
X_grid, E_grid = np.meshgrid(X, E)
f = 1 / (np.exp(beta * (E_grid - E_F)) + 1)

cmap = plt.cm.binary.copy()
cmap.set_bad(color='white')

material_ranges = [
    (-0.4, X.max()),
    (-0.1, X.max()),
    (0.3, X.max()),
    (0.6, X.max()),
    (0.9, X.max()),
    (1.3, X.max()),
]
material_E_V_values = [E_F - E_g, E_F + E_g/3, E_F - E_g/10, E_F - E_g/2, E_F - 9*E_g/10, E_F - 2*E_g]
material_E_g_values = [E_g-2, -2*E_g/3, E_g, E_g, E_g, 4*E_g]


m_e = 3.0  # Effective mass of electrons
m_h = 3.0  # Effective mass of holes

# Plot the potential distribution
fig, (ax, ax_fd) = plt.subplots(
    1,
    2,
    figsize=(20, 6),
    gridspec_kw={'width_ratios': [6, 2], 'wspace': 0.1},
    constrained_layout=True,
    sharey=True,
)

# DOS-shaped band diagram (left panel)
band_line_handles = []

for material_index, ((x_start, x_end), material_E_V, material_E_g) in enumerate(zip(material_ranges, material_E_V_values, material_E_g_values)):
    x_mask = (X >= x_start) & (X <= x_end)
    material_E_C = material_E_V + material_E_g
    D_n = m_e**(3/2) * np.sqrt(np.maximum(E - material_E_C, 0))
    D_p = m_h**(3/2) * np.sqrt(np.maximum(material_E_V - E, 0))

    x_center = x_start  
    lane_half_width = (x_end - x_start) / 2
    scale = 0.01

    x_conduction = x_center + D_n * scale
    x_valence = x_center + D_p * scale

    conduction_mask = D_n > 0
    valence_mask = D_p > 0

    valence_curve_x = np.concatenate([x_valence[valence_mask], [x_center]])
    valence_curve_E = np.concatenate([E[valence_mask], [material_E_V]])
    conduction_curve_x = np.concatenate([[x_center], x_conduction[conduction_mask]])
    conduction_curve_E = np.concatenate([[material_E_C], E[conduction_mask]])

    segment_f = f[:, x_mask]
    segment_X = X_grid[:, x_mask]
    segment_E = E_grid[:, x_mask]

    inside_valence = (
        (segment_E <= material_E_V)
        & (segment_X >= x_center)
        & (segment_X <= x_valence[:, None])
    )
    inside_conduction = (
        (segment_E >= material_E_C)
        & (segment_X >= x_center)
        & (segment_X <= x_conduction[:, None])
    )
    material_f = np.where(inside_valence | inside_conduction, segment_f, np.nan)

    image = ax.imshow(
        material_f,
        extent=[X[x_mask].min(), X[x_mask].max(), E.min(), E.max()],
        origin='lower',
        cmap=cmap,
        # alpha=0.9,
        interpolation='bicubic',
        aspect='auto',
        vmin=0,
        vmax=1,
        zorder=1,
    )

    if material_index == 1 and material_E_C < material_E_V:
        valence_outside_mask = E <= E_F
        conduction_outside_mask = E >= E_F
        ax.plot(
            x_valence[valence_outside_mask],
            E[valence_outside_mask],
            color='black',
            linewidth=1.4,
            zorder=3,
        )
        ax.plot(
            x_conduction[conduction_outside_mask],
            E[conduction_outside_mask],
            color='black',
            linewidth=1.4,
            zorder=3,
        )
    else:
        ax.plot(valence_curve_x, valence_curve_E, color='black', linewidth=1.4, zorder=3)
        ax.plot(conduction_curve_x, conduction_curve_E, color='black', linewidth=1.4, zorder=3)

    ax.vlines(x_center, E.min(), material_E_V, color='black', linewidth=1.4, zorder=3)
    ax.vlines(x_center, material_E_C, E.max(), color='black', linewidth=1.4, zorder=3)



ax.axhline(E_F, color='k', linestyle='--', label='Fermi Energy (E_F)')
ax.axhline(E_F + k_B*T, color='k', linestyle='--')
ax.axhline(E_F - k_B*T, color='k', linestyle='--')
ax.set_title('Filling of Electron States in Different Materials', fontsize=18)
# ax.set_xlabel('Density of states')
ax.set_ylabel(r'Energy ($E$)')
ax.set_yticks([E_F, E_F + k_B*T, E_F - k_B*T])
ax.set_yticklabels([r'$E_F$', r'$E_F + k_B T$', r'$E_F - k_B T$'])
ax.set_xlim(X.min(), X.max())
ax.set_ylim(E.min(), E.max())
ax.set_xticks([-0.33, -0.02, 0.38, 0.675, 0.97, 1.35])
ax.set_xticklabels([
    'Metal',
    'Semimetal',
    'p-type',
    'intrinsic\nSemiconductor',
    '(n-type)',
    'Insulator',
], fontsize=16)
ax.tick_params(axis='x', length=0, pad=14)

f_fd = 1 / (np.exp(beta * (E - E_F)) + 1)
ax_fd.plot(f_fd, E, color='blue', lw=2, label='Fermi-Dirac distribution')
ax_fd.axhline(E_F, color='k', linestyle='--', linewidth=1)
ax_fd.axhline(E_F + k_B*T, color='k', linestyle='--', linewidth=1)
ax_fd.axhline(E_F - k_B*T, color='k', linestyle='--', linewidth=1)
ax_fd.set_title('Fermi-Dirac Distribution', fontsize=18)
ax_fd.set_xlabel(r'Probability $f(E)$')
ax_fd.set_xlim(0, 1)
ax_fd.tick_params(axis='y', left=False, labelleft=False)

cbar = fig.colorbar(image, ax=ax, pad=0.01)
cbar.set_label('Electron probability')
plt.savefig(
    '1.pdf',
    format='pdf',
    bbox_inches='tight',
    # facecolor='white',
    # edgecolor='white',
    # transparent=False,
)
plt.show()

