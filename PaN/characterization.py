import numpy as np
import matplotlib.pyplot as plt

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


# IDS - VDS data
data1 = np.loadtxt("./Data-IDS-VGS/20262104001.dat")
data2 = np.loadtxt("./Data-IDS-VGS/20262104002.dat")
data3 = np.loadtxt("./Data-IDS-VGS/20262104003.dat")
data4 = np.loadtxt("./Data-IDS-VGS/20262104004.dat")
data5 = np.loadtxt("./Data-IDS-VGS/20262104005.dat")
data6 = np.loadtxt("./Data-IDS-VGS/20262104006.dat")
data7 = np.loadtxt("./Data-IDS-VGS/20262104007.dat")
data8 = np.loadtxt("./Data-IDS-VGS/20262104008.dat")
# IDS - VGS data

# IGS - VGS data

datasets_IDS_VDS = [
    ("-25 V", data8, 'cyan', 'h'),
    ("-20 V", data7, 'magenta', 'P'),
    ("-15 V", data6, 'black', 'X'),
    ("-10 V", data5, 'red', 'o'),
    ("-8 V", data4, 'blue', 's'),
    ("-6 V", data3, 'green', '^'),
    ("-4 V", data2, 'orange', 'D'),
    ("-2 V", data1, 'purple', 'v')
]
for label, data, color, marker in datasets_IDS_VDS:
    V_GS = data[:, 0]
    I_DS = data[:, 1]
    plt.plot(-V_GS, -I_DS, lw=2, label=label, color=color, marker=marker, linestyle='-', markevery=10)

plt.xlabel(r"$-V_\text{GS}$ (V)")
plt.ylabel(r"$-I_\text{DS}$ (A)")
plt.xlim(25, 45)
plt.title("Transfer Characteristics of O-FET (PaN)")
plt.legend()
plt.savefig("PaN.eps", format='eps')
plt.show()

# After that, IGS reach 1uA before reaching threshold voltage -> device defects.