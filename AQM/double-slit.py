import numpy as np
import matplotlib.pyplot as plt

# Custom settings
plt.style.use('classic')
plt.rcParams.update({
    'figure.dpi': 150,
    'figure.figsize': (8, 6),
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.linewidth': 2,
    'axes.labelsize': 15,
    'axes.labelcolor': 'black',
    'savefig.facecolor': 'white',
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial'],
    'mathtext.fontset': 'cm',

    'savefig.bbox': 'tight',
    # Ticks
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 8,
    "ytick.major.size": 8,
    "xtick.major.width": 2,
    "ytick.major.width": 2,
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "xtick.minor.size": 4,
    "ytick.minor.size": 4,
    "xtick.minor.width": 1.5,
    "ytick.minor.width": 1.5,
})


# Parameters
lamb = 500e-9  # Wavelength (m)
a = 2e-3       # Slit separation (m)
b = 0.1e-3     # Slit width (m)
L = 1          # Distance to screen (m)
# Calculate positions of interference fringes
x = np.linspace(-0.003, 0.003, 2001)  # Screen positions (m)
# Calculate intensity pattern
beta = (np.pi * a * x) / (lamb * L)
# Calculate diffraction pattern
gamma = (np.pi * b * x) / (lamb * L)
# Combine interference and diffraction patterns
I_single_slit = np.sinc(gamma)**2
I = np.cos(beta)**2 * I_single_slit
# Plotting
fig, (ax_left, ax_right) = plt.subplots(1, 2, sharey=True)


ax_left.plot(I, x, color='blue')
ax_left.plot(I_single_slit, x, color='red', linestyle='--', label='Diffraction Envelope')
ax_left.set_title('Double-Slit Interference Pattern')
# ax_left.set_xlabel('pi bx / (λL) (dimensionless)')
# ax_left.set_ylabel('Intensity (arbitrary units)')
ax_left.set_ylim(-0.003, 0.003)
ax_left.set_xlim(1.1, 0)
ax_left.set_xlabel('Normalized Intensity')
ax_left.set_ylabel('Position on Screen (m)')

image_data = I.reshape(1, -1)  # Reshape for imshow
image = ax_right.imshow(
    np.rot90(image_data),
    aspect='auto',
    origin='lower',
    cmap='hot',
    interpolation='nearest',
    extent=[0, 1.1, -0.003, 0.003],
    vmin=0,
    vmax=1,
)
ax_right.set_title('Intensity Map')
ax_right.set_xticks([])
ax_right.yaxis.tick_right()
ax_right.yaxis.set_label_position('right')
ax_right.set_ylim(-0.003, 0.003)
fig.colorbar(image, ax=ax_right, location='right')

plt.savefig('slit.eps', format='eps', bbox_inches='tight')
plt.show()

