# Simulation of charge carriers distribution in MOSFET
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

x = np.linspace(-10, 10, 100)
y = np.linspace(0, 20, 100)
X, Y = np.meshgrid(x, y)
sigma = 0.5

# Gate region

Z = np.zeros_like(Y)
gate_mask = (Y > 0) & (Y < 3)
Z[gate_mask] = 1.4-(
    np.exp(-(Y[gate_mask] - 0.0)**2 / (2 * sigma**2))
    + np.exp(-(Y[gate_mask] - 3.0)**2 / (2 * sigma**2))
    + np.exp(-(X[gate_mask] + 10.0)**2 / (2 * sigma**2))
    + np.exp(-(X[gate_mask] - 10.0)**2 / (2 * sigma**2))
)

# Insulator region
insulator_mask = (Y >= 3) & (Y < 10)
Z[insulator_mask] = (
    - np.exp(-(Y[insulator_mask] - 3.0)**2 / (2 * sigma**2))
    + np.exp(-(Y[insulator_mask] - 10.0)**2 / (2 * sigma**2))
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
