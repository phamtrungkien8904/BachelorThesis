import numpy as np
import matplotlib.pyplot as plt

# Custom settings
plt.style.use('classic')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['figure.dpi'] = 100



# IDS - VGS data
data1 = np.loadtxt("./Data-IDS-VGS/20262204001.dat")
data2 = np.loadtxt("./Data-IDS-VGS/20262204002.dat")
data3 = np.loadtxt("./Data-IDS-VGS/20262204003.dat")
data4 = np.loadtxt("./Data-IDS-VGS/20262204004.dat")
data5 = np.loadtxt("./Data-IDS-VGS/20262204005.dat")
data6 = np.loadtxt("./Data-IDS-VGS/20262204006.dat")
data7 = np.loadtxt("./Data-IDS-VGS/20262204007.dat")
data8 = np.loadtxt("./Data-IDS-VGS/20262204008.dat")
# IDS - VDS data
data9 = np.loadtxt("./Data-IDS-VDS/20262204001.dat")
data10 = np.loadtxt("./Data-IDS-VDS/20262204002.dat")
data11 = np.loadtxt("./Data-IDS-VDS/20262204003.dat")
data12 = np.loadtxt("./Data-IDS-VDS/20262204004.dat")
data13 = np.loadtxt("./Data-IDS-VDS/20262204005.dat")
data14 = np.loadtxt("./Data-IDS-VDS/20262204006.dat")

# IGS - VGS data
data15 = np.loadtxt("./Data-IGS-VGS/20262204001.dat")

# IDS-VDS Compare with Multimeter on/off
data16 = np.loadtxt("./Data-Error/20262304001.dat")
data17 = np.loadtxt("./Data-Error/20262304002.dat")


datasets_IDS_VGS = [
    # ("-40 V", data8, 'cyan', 'h'),
    # ("-30 V", data7, 'magenta', 'P'),
    # ("-20 V", data6, 'black', 'X'),
    # ("-10 V", data5, 'red', 'o'),
    ("-8 V", data4, 'blue', 's'),
    ("-6 V", data3, 'green', '^'),
    ("-4 V", data2, 'orange', 'D'),
    ("-2 V", data1, 'red', 'v')
]
for label, data, color, marker in datasets_IDS_VGS:
    V_GS = data[:, 0]
    I_DS = data[:, 1]
    plt.plot(-V_GS, -I_DS*1e6, lw=2, label=r"$V_{34} = $" + label, color=color, marker=marker, linestyle='-', markevery=40, markeredgecolor="white", markeredgewidth=1, markersize=7)

plt.xlabel(r"Gate Voltage $-V_{G4}$ (V)", fontsize=14)
plt.ylabel(r"Drain Current $-I_{34}$ ($\mu$A)", fontsize=14)
plt.xlim(0, 40)
plt.ylim(-0.1,1)
plt.title("Transfer Characteristics of O-FET (PS12)", fontsize=15)
plt.legend(frameon=True, loc='upper left', numpoints=1, fontsize=15)
plt.savefig("transfer_PS12.eps", format='eps', bbox_inches='tight')
plt.show()

datasets_IDS_VDS = [
    # ("-30 V", data14, 'cyan', 'h'),
    # ("-25 V", data13, 'magenta', 'P'),
    ("-20 V", data12, 'black', 'v'),
    ("-15 V", data11, 'red', 'o'),
    ("-10 V", data10, 'blue', 's'),
    ("-5 V", data9, 'green', '^')
]
for label, data, color, marker in datasets_IDS_VDS:
    V_DS = data[:, 0]
    I_DS = data[:, 1]
    plt.plot(-V_DS, -I_DS*1e6, lw=2, label=r"$V_{G4} = $" + label, color=color, marker=marker, linestyle='-', markevery=40, markeredgecolor="white", markeredgewidth=1, markersize=7)

plt.xlabel(r"Drain Voltage $-V_{34}$ (V)", fontsize=14)
plt.ylabel(r"Drain Current $-I_{34}$ ($\mu$A)", fontsize=14)
plt.xlim(0, 40)
plt.ylim(-0.1, 0.5)
plt.title("Output Characteristics of O-FET (PS12)", fontsize=15)
plt.legend(frameon=True, loc='upper left', numpoints=1, fontsize=15)
plt.savefig("output_PS12.eps", format='eps', bbox_inches='tight')
plt.show()

datasets_IGS_VGS = [
    ("IGS-VGS", data15, 'black', 'o')]
for label, data, color, marker in datasets_IGS_VGS:
    V_GS = data[:, 0]
    I_GS = data[:, 1]
    plt.plot(-V_GS, -I_GS*1e9, lw=2, label=label, color=color, marker=marker, linestyle='-', markevery=40)

plt.xlabel(r"$-V_{G4}$ (V)")
plt.ylabel(r"$-I_\text{GS}$ (nA)")
plt.xlim(0, 30)
plt.title("Gate Leakage Current of O-FET (PS12)")
plt.legend(frameon=True, loc='upper left', numpoints=1, fontsize=12)
plt.savefig("gate_leakage_PS12.eps", format='eps', bbox_inches='tight')
plt.show()