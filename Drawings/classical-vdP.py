import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


# ============================================================
# Plot settings
# ============================================================
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
    'figure.figsize': (5/2.54, 5/2.54),  # 10x6 cm in inches (1 figure per line)
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
    # 'figure.constrained_layout.use': True,

    # Ticks
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 4,
    "ytick.major.size": 4,
    "xtick.major.width": 1,
    "ytick.major.width": 1,
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


# Windows-only Enter-key detection
try:
    import msvcrt
except ImportError:
    msvcrt = None


def enter_pressed():
    """Return True when Enter is pressed in a Windows terminal."""
    if msvcrt is None:
        return False

    if not msvcrt.kbhit():
        return False

    while msvcrt.kbhit():
        key = msvcrt.getwch()
        if key in ("\r", "\n"):
            return True

    return False


def time_format(seconds):
    """Convert seconds to hh:mm:ss."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# ============================================================
# Simulation parameters
# ============================================================
start_time = time.time()

epsilon = 1.0

N = 201
max_iter = 100000000
step_iter = 10000
print_iter = 10000

# Relaxation factor:
# 0 < alpha <= 1
alpha = 0.05

# Relative convergence criterion in percent
tolerance = 5e-13

x = np.linspace(0.0, 1.0, N)
y = np.linspace(0.0, 1.0, N)
X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]

V = np.zeros((N, N), dtype=float)
rho = np.zeros((N, N), dtype=float)

contact_mask = np.zeros((N, N), dtype=bool)

# ============================================================
# Contact definition
# ============================================================
contact_size = 0.1
contact_width = max(1, int(round(contact_size * N)))

# Contacts at the lower-left and upper-left corners
V[:contact_width, :contact_width] = 5.0
V[-contact_width:, :contact_width] = -5.0

contact_mask[:contact_width, :contact_width] = True
contact_mask[-contact_width:, :contact_width] = True

# Preserve fixed contact voltages
contact_V = V.copy()


# ============================================================
# Poisson solver
# ============================================================
def solve(V_initial, rho):
    V = V_initial.copy()

    # Store the convergence error for every iteration
    error_history = np.empty(max_iter, dtype=float)

    print("Press Enter in the terminal to stop early.")

    final_iteration = max_iter

    for i in range(max_iter):
        V_old = V.copy()
        V_new = V.copy()

        # ----------------------------------------------------
        # Jacobi update for
        #
        #     ∇²V = -rho / epsilon
        #
        # Therefore:
        #
        # V(i,j) = 1/4 * [neighbors + dx² rho/epsilon]
        # ----------------------------------------------------
        V_new[1:-1, 1:-1] = 0.25 * (
            V_old[2:, 1:-1]
            + V_old[:-2, 1:-1]
            + V_old[1:-1, 2:]
            + V_old[1:-1, :-2]
            + dx**2 * rho[1:-1, 1:-1] / epsilon
        )

        # ----------------------------------------------------
        # Neumann outer boundaries: dV/dn = 0
        # ----------------------------------------------------
        V_new[0, :] = V_new[1, :]
        V_new[-1, :] = V_new[-2, :]
        V_new[:, 0] = V_new[:, 1]
        V_new[:, -1] = V_new[:, -2]

        # Restore Dirichlet conditions at contacts
        V_new[contact_mask] = contact_V[contact_mask]

        # ----------------------------------------------------
        # Under-relaxation
        # ----------------------------------------------------
        V = (1.0 - alpha) * V_old + alpha * V_new

        # Ensure that numerical relaxation never modifies
        # the prescribed contact voltages
        V[contact_mask] = contact_V[contact_mask]

        # ----------------------------------------------------
        # Relative convergence error in percent
        # ----------------------------------------------------
        absolute_change = np.max(np.abs(V - V_old))

        reference_value = max(
            np.max(np.abs(V_old)),
            np.max(np.abs(V)),
            1e-30,
        )

        error_percent = 100.0 * absolute_change / reference_value
        error_history[i] = error_percent

        if (i + 1) % print_iter == 0:
            print(
                f"\rStep {i + 1}/{max_iter}, "
                f"Error: {error_percent:.6e} %"
            )

        # Convergence check
        if error_percent <= tolerance:
            final_iteration = i + 1
            elapsed_time = time.time() - start_time

            print(
                f"\nConverged at iteration: "
                f"{final_iteration}/{max_iter}, "
                f"Error: {error_percent:.2e} %, "
                f"Runtime: {time_format(elapsed_time)}"
            )
            break

        # Manual stopping
        if enter_pressed():
            final_iteration = i + 1
            elapsed_time = time.time() - start_time

            print(
                f"\nStopped by user at iteration: "
                f"{final_iteration}/{max_iter}, "
                f"Error: {error_percent:.2e} %, "
                f"Runtime: {time_format(elapsed_time)}"
            )
            break

        # Runtime information
        if (i + 1) % step_iter == 0:
            elapsed_time = time.time() - start_time

            print(
                f"\rIteration: {i + 1}/{max_iter}, "
                f"Error: {error_percent:.2e} %, "
                f"Runtime: {time_format(elapsed_time)}",
                end="",
            )

    # Keep only the calculated part of the array
    error_history = error_history[:final_iteration]

    return V, rho, error_history


V, rho, error_history = solve(V, rho)
dV_dy, dV_dx = np.gradient(V, dy, dx)

E_x = -dV_dx
E_y = -dV_dy
E_magnitude = np.hypot(E_x, E_y)

# Normalize arrows so that quiver mainly displays direction.
# The electric-field strength is still contained in E_magnitude.
E_x_normalized = np.divide(
    E_x,
    E_magnitude,
    out=np.zeros_like(E_x),
    where=E_magnitude > 1e-15,
)

E_y_normalized = np.divide(
    E_y,
    E_magnitude,
    out=np.zeros_like(E_y),
    where=E_magnitude > 1e-15,
)

# Do not draw arrows inside the fixed-voltage contacts
E_x_normalized[contact_mask] = np.nan
E_y_normalized[contact_mask] = np.nan


end_time = time.time()
print(f"\nExecution time: {end_time - start_time:.2f} seconds.")



# ============================================================
# 2D potential, equipotential lines and electric-field quiver
# ============================================================
fig2D_potential = plt.figure(figsize=(7/2.54, 5/2.54))
ax2D = fig2D_potential.add_subplot(111)
# Reserve space on the right for the colorbar and its label
# fig2D_potential.subplots_adjust(
#     left=0.02,
#     right=0.82,
#     bottom=0.05,
#     top=0.95,
# )


image = ax2D.imshow(
    V,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="jet",
    interpolation="bicubic",
    vmin=V.min(),
    vmax=V.max(),
    zorder=1,
)

divider = make_axes_locatable(ax2D)

cax = divider.append_axes(
    "right",
    size="5%",   # colorbar width
    pad=0.1,    # distance from plot
)

# Reduce height to 3/4 and center vertically
fig2D_potential.canvas.draw()

ax_pos = ax2D.get_position()
cax_pos = cax.get_position()

new_height = 0.6 * ax_pos.height
new_bottom = ax_pos.y0 + 0.2 * ax_pos.height

cax.set_axes_locator(None)
cax.set_position([
    cax_pos.x0,
    new_bottom,
    cax_pos.width,
    new_height,
])
cbar = fig2D_potential.colorbar(
    image,
    cax=cax,
    label="Potential (V)",
)

cbar.set_label("Potential (V)")


# ============================================================
# Equipotential lines
# ============================================================

# Approximate centers of the two contacts on the right side
lower_probe_row = contact_width // 2
upper_probe_row = N - 1 - contact_width // 2
right_probe_column = N - 1

# Potential at the two right-side probe positions
V_right_lower = V[lower_probe_row, right_probe_column]
V_right_upper = V[upper_probe_row, right_probe_column]

special_levels = np.sort([
    V_right_lower,
    V_right_upper,
])

# Ordinary equipotential lines
all_levels = np.linspace(V.min(), V.max(), 17)[1:-1]

level_tolerance = max(
    1e-12,
    1e-6 * (V.max() - V.min()),
)

regular_levels = np.array([
    level
    for level in all_levels
    if np.all(np.abs(level - special_levels) > level_tolerance)
])

if regular_levels.size > 0:
    ax2D.contour(
        X,
        Y,
        V,
        levels=regular_levels,
        colors="black",
        linewidths=0.5,
        linestyles="--",
        alpha=0.75,
        zorder=2,
    )

# Two thicker equipotential lines through the right contacts
if not np.isclose(
    V_right_lower,
    V_right_upper,
    atol=level_tolerance,
    rtol=0.0,
):
    ax2D.contour(
        X,
        Y,
        V,
        levels=special_levels,
        colors="black",
        linewidths=1.0,
        linestyles="solid",
        zorder=3,
    )
else:
    ax2D.contour(
        X,
        Y,
        V,
        levels=[0.5 * (V_right_lower + V_right_upper)],
        colors="black",
        linewidths=2.0,
        linestyles="solid",
        zorder=3,
    )


# ============================================================
# Electric-field quiver
# ============================================================

# Draw only every nth grid point to avoid overcrowding
quiver_step = 10

ax2D.quiver(
    X[::quiver_step, ::quiver_step],
    Y[::quiver_step, ::quiver_step],
    E_x_normalized[::quiver_step, ::quiver_step],
    E_y_normalized[::quiver_step, ::quiver_step],
    color="black",
    angles="xy",
    scale_units="xy",
    scale=25,
    width=0.002,
    headwidth=5.5,
    headlength=6.5,
    headaxislength=4.0,
    pivot="middle",
    zorder=4,
)

# ax2D.set_aspect("equal")
ax2D.set_xlim(0.0, 1.0)
ax2D.set_ylim(0.0, 1.0)
ax2D.set_axis_off()

plt.savefig("classical-vdP.pdf", dpi=300)
plt.savefig("classical-vdP.eps")
plt.show()