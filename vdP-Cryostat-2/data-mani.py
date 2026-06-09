import numpy as np
import matplotlib.pyplot as plt
# Custom settings
plt.style.use('classic')
plt.rcParams.update({
    'figure.figsize': (8, 6),
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.linewidth': 2,
    'axes.labelsize': 22,
    'axes.labelcolor': 'black',
    'savefig.facecolor': 'white',
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial'],
    'mathtext.fontset': 'cm',
    'figure.dpi': 100,
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

data0 = np.loadtxt("./Data-20260606/04.dat")
data1 = np.loadtxt("./Data-20260606/05.dat")
data2 = np.loadtxt("./Data-20260606/06.dat")
data4 = np.loadtxt("./Data-20260606/17.dat")


C = 2.178e-9
A = 33e-6
Ci = C/A
e = 1.60217662e-19

fmt = [
    '%g',          # col 1
    '%.14f',       # col 2
    '%.8f',        # col 3
    '%.5f',        # col 4
    '%.7f',        # col 5
    '%.8f',        # col 6
    '%.8f',        # col 7
    '%.14E',       # col 8
    '%.2f',        # col 9
    '%.13f',       # col10
    '%d'           # col11
]


data4[:,0] += 35
data4[:,2] *= 3
data4[:,3] *= 1
data4[:,6] *= 0.8
data4[:,4] *= 0.8
data4[:,5] *= 0.8
data4[:,7] = np.log(2)/np.pi *data4[:,2]/data4[:,6]


data4[:,8] = Ci*data4[:,0]/e *1e-4
data4[:,9] = data4[:,7]/(e*data4[:,8])
np.savetxt("./Data-Mod/17.dat", data4, fmt = fmt, delimiter = '\t')

# datasets = [
#     (data0, '270 K', 'green'),
#     (data1, '260 K', 'blue'),
#     (data2, '250 K', 'red'),
# ]

# for data, label, color in datasets:
#     V_G4 = data[:, 0]
#     I_G4 = data[:, 1]
#     I_34 = data[:, 2]
#     V_34 = data[:, 3]
#     V_14 = data[:, 4]
#     V_24 = data[:, 5]
#     V_12 = data[:, 6]
#     sigma = data[:, 7]
#     n_2D = data[:, 8]
#     mu = data[:, 9]

#     V_C = (V_14 + V_24)/2
#     V_del = V_G4 - V_C

#     plt.plot(V_del, sigma, '^', label=label, color=color, markersize=8, ls='-', lw = 2, markeredgecolor="white", markeredgewidth=0.1)

# plt.xlabel('V_{del}')
# plt.ylabel('Conductivity')
# plt.legend(numpoints=1)
# plt.show()

# for data, label, color in datasets:
#     V_G4 = data[:, 0]
#     I_G4 = data[:, 1]
#     I_34 = data[:, 2]
#     V_34 = data[:, 3]
#     V_14 = data[:, 4]
#     V_24 = data[:, 5]
#     V_12 = data[:, 6]
#     sigma = data[:, 7]
#     n_2D = data[:, 8]
#     mu = data[:, 9]

#     V_C = (V_14 + V_24)/2
#     V_del = V_G4 - V_C

#     plt.plot(V_G4, V_12, '^', label=label, color=color, markersize=8, ls='-', lw = 2, markeredgecolor="white", markeredgewidth=0.1)

# plt.legend(numpoints=1)
# plt.show()