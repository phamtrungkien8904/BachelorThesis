import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

N = 10000 # Resolution of the grid
N = 100 # Resolution of the grid
x = np.linspace(-10, 10, N)
y = np.linspace(0, 20, N)
X, Y = np.meshgrid(x, y)

# Gate region

Z = np.zeros_like(Y)
gate_mask = (Y > 0) & (Y < 3) & (X > -10) & (X < 10)
Z[gate_mask] = -np.exp(-(Y[gate_mask] - 1.5)**2 / (2 * 1.5**2)-X[gate_mask]**2 / (2 * 9.5**2))

# Insulator region
insulator_mask = (Y >= 3) & (Y < 10)
Z[insulator_mask] = (
    + np.exp(-(Y[insulator_mask] - 3.0)**2 / (2 * 0.5**2))
    - np.exp(-(Y[insulator_mask] - 10.0)**2 / (2 * 0.5**2))
)


cmap = mpl.colors.LinearSegmentedColormap.from_list(
    'blue_white_red', ['blue', 'white', 'red']
)
norm = mpl.colors.TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
plt.contourf(X, Y, Z, levels=50, cmap=cmap, norm=norm)
plt.gca().set_aspect('equal', adjustable='box')
plt.colorbar(label='Z value')
plt.title('Simulation of charge carriers distribution in MOSFET')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
