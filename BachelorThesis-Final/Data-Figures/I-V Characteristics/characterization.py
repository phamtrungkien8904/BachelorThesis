import numpy as np
import matplotlib.pyplot as plt

# Custom settings
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

# IDS - VGS data
data1 = np.loadtxt("./Data-IDS-VGS/20262504001.dat")
data2 = np.loadtxt("./Data-IDS-VGS/20262504002.dat")
data3 = np.loadtxt("./Data-IDS-VGS/20262504003.dat")
data4 = np.loadtxt("./Data-IDS-VGS/20262504004.dat")
data5 = np.loadtxt("./Data-IDS-VGS/20262504005.dat")
data6 = np.loadtxt("./Data-IDS-VGS/20262504006.dat")

# IDS - VDS data
data7 = np.loadtxt("./Data-IDS-VDS/20262504001.dat")
data8 = np.loadtxt("./Data-IDS-VDS/20262504002.dat")
data9 = np.loadtxt("./Data-IDS-VDS/20262504003.dat")
data10 = np.loadtxt("./Data-IDS-VDS/20262504004.dat")
data11 = np.loadtxt("./Data-IDS-VDS/20262504005.dat")
data12 = np.loadtxt("./Data-IDS-VDS/20262504006.dat")

# IGS - VGS data
data13 = np.loadtxt("./Data-IGS-VGS/20262504001.dat")

datasets_IDS_VGS = [
    # ("-30", data6, 'cyan', 'h'),
    # ("-25", data5, 'magenta', 'P'),
    ("-20", data4, 'black', 'v'),
    ("-15", data3, 'red', 'o'),
    ("-10", data2, 'blue', 's'),
    ("-5", data1, 'green', '^'),
]

for label, data, color, marker in datasets_IDS_VGS:
    V_GS = data[:, 0]
    I_DS = data[:, 1]
    plt.plot(-V_GS, -I_DS*1e6, label=label, color=color, marker=marker, markevery=20)

plt.xlabel(r"Gate Voltage $-V_\text{G4}$ (V)")
plt.ylabel(r"Drain Current $-I_{34}$ ($\mu$A)")
plt.xlim(0, 40)
plt.ylim(-0.1, 1.0)
plt.title("Transfer Characteristics of O-FET")
plt.legend(loc='upper left', title=r"$V_\text{34}$ (V)")
plt.savefig("transfer_PS9.eps", format='eps')
plt.show()

datasets_IDS_VDS = [
    # ("-30 V", data7, 'cyan', 'h'),
    # ("-25 V", data8, 'magenta', 'P'),
    ("-20", data9, 'black', 'v'),
    ("-15", data10, 'red', 'o'),
    ("-10", data11, 'blue', 's'),
    ("-5", data12, 'green', '^')
]
for label, data, color, marker in datasets_IDS_VDS:
    V_DS = data[:, 0]
    I_DS = data[:, 1]
    plt.plot(-V_DS, -I_DS*1e6, label=label, color=color, marker=marker,markevery=20)

plt.xlabel(r"Drain Voltage $-V_{34}$ (V)")
plt.ylabel(r"Drain Current $-I_{34}$ ($\mu$A)")
plt.xlim(0, 40)
plt.ylim(-0.1, 0.5)
plt.title("Output Characteristics of O-FET")
plt.legend(loc='upper left', title=r"$V_\text{G4}$ (V)")
plt.savefig("output_PS9.eps", format='eps')
plt.show()

datasets_IGS_VGS = [
    ("IGS-VGS", data13, 'red', 'o')]
for label, data, color, marker in datasets_IGS_VGS:
    V_GS = data[:, 0]
    I_GS = data[:, 1]
    plt.plot(-V_GS, -I_GS*1e9,label=label, color=color)

plt.xlabel(r"Gate Voltage $-V_\text{G4}$ (V)")
plt.ylabel(r"Leakage Gate Current $-I_\text{G4}$ (nA)")
plt.ylim(0,1)
plt.xlim(0, 40)
plt.title("Gate Leakage Current of O-FET")
# plt.legend(loc='upper left')
plt.savefig("leakage_PS9.eps", format='eps')
plt.show()