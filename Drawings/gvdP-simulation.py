import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable



# Custom settings for python figures
plt.style.use('classic')

plt.rcParams.update({
    "text.usetex": True,
    'text.latex.preamble': r'''
    \usepackage[T1]{fontenc}
    \usepackage{lmodern}
    \usepackage[utf8]{inputenc}
    \usepackage{amsmath}
    \usepackage{amssymb}
    \usepackage{siunitx}
    \usepackage{sfmath}
    '''
})
plt.rcParams.update({
    # Figure settings
    'figure.dpi': 300,
    'figure.figsize': (10/2.54, 6/2.54),  # 10x6 cm in inches (1 figure per line)
    # 'figure.figsize': (8/2.54, 6/2.54),  # 10x6 cm in inches (2 figures per line)
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.linewidth': 1,
    'axes.labelsize': 8,
    'axes.titlesize': 8,
    'axes.labelcolor': 'black',
    'savefig.facecolor': 'white',
    'font.family': 'sans-serif',
    'font.sans-serif': 'Arial',
    # 'mathtext.fontset': 'cm',
    'figure.constrained_layout.use': True,

    # Ticks
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 4,
    "ytick.major.size": 4,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "xtick.minor.size": 0,
    "ytick.minor.size": 0,
    "xtick.minor.width":0,
    "ytick.minor.width": 0,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,  

    # Legend
    'legend.frameon': False,
    'legend.title_fontsize': 8,
    'legend.fontsize': 8,
    'legend.handlelength': 2,
    'legend.loc': 'best',
    'legend.numpoints': 1,

    # Line style
    'lines.linestyle': '-',
    'lines.linewidth': 1,
    'lines.markersize': 4,
    'lines.markeredgecolor': 'white',
    'lines.markeredgewidth': 0.5,
})


# ----------------------------------------------------------------------
# User parameters
# ----------------------------------------------------------------------
File_index = "01"

N = 201                      # grid points in x and y direction
L = 1000e-9                   # square side length [m]
# Contact geometry: four small square corner regions.
# Current is injected/sunk between contacts 1 and 2; contacts 3 and 4 are
# passive probe regions for reading V3 and V4.
contact_size = 0.08          # fraction of side length
contact_width = max(2, int(contact_size * N))

# ----------------------------------------------------------------------
# Physical constants and material parameters
# ----------------------------------------------------------------------
k_B = 1.380649e-23           # Boltzmann constant [J/K]
T = 300.0                    # temperature [K]
e = 1.602176634e-19          # elementary charge [C]
epsilon = 3.0 * 8.854187817e-12
mu = 1e-4                    # hole mobility [m^2/(V s)] = 1 cm^2/(V s)

Vth = k_B * T / e

# Voltages
V_bi = 5.0 * Vth            # built-in potential [V]
V_D = -10.0 * Vth            # contact-2 voltage relative to contact 1 [V]
V_G = 0.0 * Vth              # uniform gate voltage [V]

# Semiconductor parameters
N_A = 1e21                   # acceptor / neutral background density [m^-3]
N_v = 1e25                   # effective valence DOS [m^-3]

# Choose F boundary such that at contact 1 with phi=0:
# p_contact1 = Nv exp[-(F_contact1 - e V_G)/(kBT)] = NA exp(V_bi/Vth)
E_B = e * Vth * np.log(N_v / N_A) - e * V_bi  # [J]
p_contact1 = N_v * np.exp(-(E_B - e * V_G) / (k_B * T))

# ----------------------------------------------------------------------
# Grid and arrays
# ----------------------------------------------------------------------
x = np.linspace(0.0, L, N)
y = np.linspace(0.0, L, N)
dx = x[1] - x[0]
dy = y[1] - y[0]
X, Y = np.meshgrid(x, y)


################# Data Extract
V = np.loadtxt(f"./Data-Export/VDP/VDP_Poti_{File_index}.dat")
p = np.loadtxt(f"./Data-Export/VDP/VDP_Holes_{File_index}.dat")



PLOT_RESULTS = True

if PLOT_RESULTS:
    x_nm = x * 1e6
    y_nm = y * 1e6

    extent_nm = [
        x_nm.min(),
        x_nm.max(),
        y_nm.min(),
        y_nm.max(),
    ]

    # One figure containing two 2D plots
    fig, (ax_pot, ax_hole) = plt.subplots(
        1,
        2,
        figsize=(16/2.54, 7/2.54),  # 14x6 cm in inches (1 figure per line)
        constrained_layout=True,
    )
    # fig.set_constrained_layout_pads(
    #     wspace=0.05,   # increase or decrease this value
    # )
    
    # ==============================================================
    # 2D potential distribution
    # ==============================================================
    im_pot = ax_pot.imshow(
        V,
        extent=extent_nm,
        origin="lower",
        interpolation="bicubic",
        aspect="equal",
        cmap="jet",
    )
    

    cbar_pot = fig.colorbar(
        im_pot,
        ax=ax_pot,
        shrink=0.5,
        pad=0.01,
    )
    cbar_pot.ax.tick_params(axis="y", pad=1)

    ax_pot.set_xlabel(r"$x$-position ($\mathrm{\mu m}$)")
    ax_pot.set_ylabel(r"$y$-position ($\mathrm{\mu m}$)")
    ax_pot.set_title("Potential distribution")

    # Optional equipotential lines
    # ax_pot.contour(
    #     X * 1e9,
    #     Y * 1e9,
    #     V,
    #     levels=12,
    #     colors="k",
    #     linewidths=0.5,
    # )

    # ==============================================================
    # 2D hole-density distribution
    # ==============================================================
    im_hole = ax_hole.imshow(
        np.maximum(p, 1.0),
        extent=extent_nm,
        origin="lower",
        interpolation="bicubic",
        aspect="equal",
        cmap="viridis",
        vmax = np.max(p/5),
    )

    cbar_hole = fig.colorbar(
        im_hole,
        ax=ax_hole,
        shrink=0.5,
        pad=0.01,
    )
    
    fig.canvas.draw()
    offset_text = cbar_hole.ax.yaxis.get_offset_text()
    offset_text.set_x(1.3)
    offset_text.set_ha("left")

    ax_hole.set_xlabel(r"$x$-position ($\mathrm{\mu m}$)")
    ax_hole.set_ylabel(r"$y$-position ($\mathrm{\mu m}$)")
    ax_hole.set_title("Hole density distribution")



    # Save figures
    plt.savefig(f"gvdP-simulation.pdf")
    plt.savefig(f"gvdP-simulation.eps")

    plt.show()