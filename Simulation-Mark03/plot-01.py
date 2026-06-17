import os
import time

import matplotlib.pyplot as plt
import numpy as np

try:
    import msvcrt
except ImportError:  # Linux/macOS/Jupyter
    msvcrt = None

# ----------------------------------------------------------------------
# Plot style
# ----------------------------------------------------------------------
plt.style.use("classic")
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["axes.edgecolor"] = "black"
plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams["savefig.facecolor"] = "white"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial"]
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["figure.dpi"] = 100

# ----------------------------------------------------------------------
# User parameters
# ----------------------------------------------------------------------
File_index = "04"

N = 51                      # grid points in x and y direction
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
Jx = np.loadtxt(f"./Data-Export/VDP/VDP_CurrentDensity_X_{File_index}.dat")
Jy = np.loadtxt(f"./Data-Export/VDP/VDP_CurrentDensity_Y_{File_index}.dat")
Jabs = np.loadtxt(f"./Data-Export/VDP/VDP_CurrentDensity_Abs_{File_index}.dat")



PLOT_RESULTS = True

if PLOT_RESULTS:
    x_nm = x * 1e9
    y_nm = y * 1e9
    extent_nm = [x_nm.min(), x_nm.max(), y_nm.min(), y_nm.max()]

    # Potential map
    fig_pot= plt.figure(figsize=(10, 8), constrained_layout=True)
    gs_pot = fig_pot.add_gridspec(1, 2, width_ratios=[1, 1.05])

    ax2D_pot = fig_pot.add_subplot(gs_pot[0, 0])
    im_pot = ax2D_pot.imshow(
        V,
        extent=extent_nm,
        origin="lower",
        interpolation="bicubic",
        aspect="equal",
    )
    fig_pot.colorbar(im_pot, ax=ax2D_pot, label=r"$\phi$ [V]", shrink=0.4)
    # ax2D_pot.contour(X * 1e9, Y * 1e9, V, levels=12, colors="k", linewidths=0.5)
    ax2D_pot.set_xlabel("x-position [nm]")
    ax2D_pot.set_ylabel("y-position [nm]")
    ax2D_pot.set_title("2D electrostatic potential")

    ax3D_pot = fig_pot.add_subplot(gs_pot[0, 1], projection="3d")
    surf_pot = ax3D_pot.plot_surface(
        X * 1e9,
        Y * 1e9,
        V,
        cmap="jet",
        rcount=N // 8,
        ccount=N // 8,
        linewidth=1,
        color="k",
        antialiased=True,
    )
    fig_pot.colorbar(surf_pot, ax=ax3D_pot, label=r"$\phi$ [V]", shrink=0.4, pad=0.08)  
    ax3D_pot.set_xlabel("x-position [nm]")
    ax3D_pot.set_ylabel("y-position [nm]")
    ax3D_pot.set_zlabel(r"$\phi$ [V]")
    ax3D_pot.set_title("3D electrostatic potential")
    
    fig_pot.suptitle("Electrostatic Potential Distribution")

    # Hole density map
    fig_hole = plt.figure(figsize=(10, 8), constrained_layout=True)
    gs_hole = fig_hole.add_gridspec(1, 2, width_ratios=[1, 1.05])
    
    ax2D_hole = fig_hole.add_subplot(gs_hole[0, 0])
    im_hole = ax2D_hole.imshow(
        np.maximum(p, 1.0),
        extent=extent_nm,
        origin="lower",
        interpolation="bicubic",
        aspect="equal",
    )
    fig_hole.colorbar(im_hole, ax=ax2D_hole, label=r"$\log_{10}(p/\mathrm{m}^{-3})$", shrink=0.4)
    ax2D_hole.set_xlabel("x-position [nm]")
    ax2D_hole.set_ylabel("y-position [nm]")
    ax2D_hole.set_title("2D hole density")

    ax3D_hole = fig_hole.add_subplot(gs_hole[0, 1], projection="3d")
    surf_hole = ax3D_hole.plot_surface(
        X * 1e9,
        Y * 1e9,    
        np.maximum(p, 1.0),
        cmap="jet",
        rcount=N // 8,
        ccount=N // 8,
        linewidth=1,
        color="k",
        antialiased=True,
    )
    fig_hole.colorbar(surf_hole, ax=ax3D_hole, label=r"$p/\mathrm{m}^{-3}$", shrink=0.4, pad=0.08)
    ax3D_hole.set_xlabel("x-position [nm]")
    ax3D_hole.set_ylabel("y-position [nm]")
    ax3D_hole.set_zlabel(r"$p/\mathrm{m}^{-3}$")
    ax3D_hole.set_title("3D hole density")
    fig_hole.suptitle("Hole Density Distribution")

    # Current streamlines and magnitude
    fig_J = plt.figure(figsize=(10, 8), constrained_layout=True)
    gs_J = fig_J.add_gridspec(1, 2, width_ratios=[1, 1.05])
    ax2D_J = fig_J.add_subplot(gs_J[0, 0])

    im_J = ax2D_J.imshow(
        np.maximum(Jabs, 1e-300),
        extent=extent_nm,
        origin="lower",
        interpolation="bicubic",
        aspect="equal",
    )
    fig_J.colorbar(im_J, ax=ax2D_J, label=r"$|J|$ [A/m$^2$]", shrink=0.4)
    ax2D_J.set_xlabel("x-position [nm]")
    ax2D_J.set_ylabel("y-position [nm]")
    ax2D_J.set_title("Current density magnitude and streamlines")

    ax3D_J = fig_J.add_subplot(gs_J[0, 1], projection="3d")
    surf_J = ax3D_J.plot_surface(
        X * 1e9,
        Y * 1e9,
        np.maximum(Jabs, 1e-300),
        cmap="jet",
        rcount=N // 8,
        ccount=N // 8,
        linewidth=1,
        color="k",
        antialiased=True,
    )
    fig_J.colorbar(surf_J, ax=ax3D_J, label=r"$|J|$ [A/m$^2$]", shrink=0.4, pad=0.08)
    ax3D_J.set_xlabel("x-position [nm]")
    ax3D_J.set_ylabel("y-position [nm]")
    ax3D_J.set_zlabel(r"$|J|$ [A/m$^2$]")
    ax3D_J.set_title("3D current density magnitude")
    fig_J.suptitle("Current Density Distribution")

    plt.show()
