import numpy as np
import matplotlib.pyplot as plt

# Custom settings
plt.style.use('classic')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['font.weight'] = 'normal'
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.sans-serif'] = ["Arial"]
plt.rcParams['mathtext.fontset'] = 'dejavusans'
plt.rcParams['figure.dpi'] = 100

# IDS - VDS data
data9 = np.loadtxt("./Data-IDS-VDS/20262204001.dat")
data10 = np.loadtxt("./Data-IDS-VDS/20262204002.dat")
data11 = np.loadtxt("./Data-IDS-VDS/20262204003.dat")
data12 = np.loadtxt("./Data-IDS-VDS/20262204004.dat")
data13 = np.loadtxt("./Data-IDS-VDS/20262204005.dat")
data14 = np.loadtxt("./Data-IDS-VDS/20262204006.dat")

datasets_IDS_VDS = [
    ("-30 V", data14, 'cyan', 'h'),
    ("-25 V", data13, 'magenta', 'P'),
    ("-20 V", data12, 'black', 'X'),
    ("-15 V", data11, 'red', 'o'),
    ("-10 V", data10, 'blue', 's'),
    ("-5 V", data9, 'green', '^')
]
for label, data, color, marker in datasets_IDS_VDS:
    V_DS = data[:, 0]
    I_DS = data[:, 1]
    plt.plot(-V_DS, -I_DS*1e6, lw=2, label=r"$V_\text{GS} = $" + label, color=color, marker=marker, linestyle='-', markevery=40)

plt.xlabel(r"$-V_\text{DS}$ (V)")
plt.ylabel(r"$-I_\text{DS}$ ($\mu$A)")
plt.xlim(0, 40)
# plt.ylim(-0.1, 1.0)
plt.title("Output Characteristics of O-FET (PS12)")
plt.legend(frameon=True, loc='upper left', numpoints=1, fontsize=12)
plt.savefig("test.eps", format='eps',bbox_inches='tight')

plt.show()