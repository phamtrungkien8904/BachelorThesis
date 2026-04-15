import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('Test20261504002.dat')

# Remove trailing placeholder rows where all values are zero.
valid_rows = np.any(data != 0, axis=1)
data = data[valid_rows]

V_GS = data[:, 0]
I_GS = data[:, 1]
V_DS = data[:, 2]
I_DS = data[:, 3]
conductivity_gs = data[:, 4]
resistivity_gs = data[:, 5]

fig, axes = plt.subplots(3, 2, figsize=(12, 10), constrained_layout=True)

plots = [
	(V_GS, 'V_GS'),
	(I_GS, 'I_GS'),
	(V_DS, 'V_DS'),
	(I_DS, 'I_DS'),
	(conductivity_gs, 'Conductivity GS'),
	(resistivity_gs, 'Resistivity GS'),
]

for ax, (series, title) in zip(axes.flat, plots):
	ax.plot(V_GS, series, linewidth=1.5)
	ax.set_title(title)
	ax.set_xlabel('V_GS')
	ax.set_ylabel(title)
	ax.grid(True, alpha=0.3)

plt.show()
