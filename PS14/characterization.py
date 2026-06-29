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
    'figure.dpi': 300,
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
    # ("-30 V", data6, 'cyan', 'h'),
    # ("-25 V", data5, 'magenta', 'P'),
    ("-20 V", data4, 'black', 'v'),
    ("-15 V", data3, 'red', 'o'),
    ("-10 V", data2, 'blue', 's'),
    ("-5 V", data1, 'green', '^'),
]
plt.figure(figsize=(8, 8))

for label, data, color, marker in datasets_IDS_VGS:
    V_GS = data[:, 0]
    I_DS = data[:, 1]
    plt.plot(-V_GS, -I_DS*1e6, label=r"$V_{34} = $" + label, color=color, marker=marker, ls='-', lw=2, markevery=20,markeredgecolor="white", markeredgewidth=1, markersize=7)

plt.xlabel(r"Gate Voltage $-V_\text{G4}$ (V)", fontsize=19)
plt.ylabel(r"Drain Current $-I_{34}$ ($\mu$A)", fontsize=19)
plt.xlim(0, 40)
plt.ylim(-0.1, 1.0)
plt.title("Transfer Characteristics of O-FET (PS14)", fontsize=20)
plt.legend(frameon=True, loc='upper left', numpoints=1, fontsize=15)
plt.savefig("transfer_PS14.eps", format='eps', bbox_inches='tight')
plt.show()a

datasets_IDS_VDS = [
    # ("-30 V", data7, 'cyan', 'h'),
    # ("-25 V", data8, 'magenta', 'P'),
    ("-20 V", data9, 'black', 'v'),
    ("-15 V", data10, 'red', 'o'),
    ("-10 V", data11, 'blue', 's'),
    ("-5 V", data12, 'green', '^')
]
plt.figure(figsize=(8, 8))
for label, data, color, marker in datasets_IDS_VDS:
    V_DS = data[:, 0]
    I_DS = data[:, 1]
    plt.plot(-V_DS, -I_DS*1e6, label=r"$V_\text{G4} = $" + label, color=color, marker=marker, ls='-', lw=2, markevery=20,markeredgecolor="white", markeredgewidth=1, markersize=7)

plt.xlabel(r"Drain Voltage $-V_{34}$ (V)", fontsize=19)
plt.ylabel(r"Drain Current $-I_{34}$ ($\mu$A)", fontsize=19)
plt.xlim(0, 40)
plt.ylim(-0.1, 0.5)
plt.title("Output Characteristics of O-FET (PS14)", fontsize=20)
plt.legend(frameon=True, loc='upper left', numpoints=1, fontsize=15)
plt.savefig("output_PS14.eps", format='eps', bbox_inches='tight')
plt.show()

datasets_IGS_VGS = [
    ("IGS-VGS", data13, 'black', 'o')]
for label, data, color, marker in datasets_IGS_VGS:
    V_GS = data[:, 0]
    I_GS = data[:, 1]
    plt.plot(-V_GS, -I_GS*1e9,label=label, color=color, marker=marker, ls='-', lw=2, markevery=40,markeredgecolor="white", markeredgewidth=1, markersize=7)

plt.xlabel(r"Gate Voltage $-V_\text{G4}$ (V)", fontsize=14)
plt.ylabel(r"Leakage Gate Current $-I_\text{G4}$ (nA)", fontsize=14)
# plt.xlim(0, 30)
plt.title("Gate Leakage Current of O-FET (PS14)", fontsize=15)
plt.legend(frameon=True, loc='upper left', numpoints=1, fontsize=12)
plt.show()