import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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



data1 = np.loadtxt("./Data_20262904/20262904005.snp") # 40V
data2 = np.loadtxt("./Data_20262904/20262904004.snp") # 35V
data3 = np.loadtxt("./Data_20262904/20262904001.snp") # 30V
data4 = np.loadtxt("./Data_20262904/20262904002.snp") # 25V
data5 = np.loadtxt("./Data_20262904/20262904003.snp") # 20V
data6 = np.loadtxt("./Data_20262904/20262904006.snp") # 15V
data7 = np.loadtxt("./Data_20262904/20262904007.snp") # 10V

dataset = [
    ("-40 V", -40, data1, 'red', 'o'),
    ("-35 V", -35, data2, 'orange', '^'),
    ("-30 V", -30, data3, 'green', 's'),
    ("-25 V", -25, data4, 'blue', 'D'),
    # ("-20 V", -20, data5, 'purple'),
    # ("-15 V", -15, data6, 'brown'),
    # ("-10 V", -10, data7, 'cyan')
]


R1 = 1e6  # 1 MΩ
R2 = 1e5 # 100 kΩ



for label, voltage, data, color, marker in dataset:
    t = data[:, 0]
    V_discharge = data[:, 2]
    I_discharge = V_discharge/R2
    V_charge = data[:, 1]
    I_charge = V_charge/R2
    Q_charge = np.abs(np.trapezoid(I_charge, t))
    Q_discharge = np.abs(np.trapezoid(I_discharge, t))
    plt.plot(t*1e3, -I_charge*1e6, label=label + f": C = {-Q_charge/voltage*1e9:.2f} nF", color=color,markevery=400, marker=marker)

plt.axhline(y=0.0, color='black', ls='--', lw=0.5)
plt.xlabel('Time (ms)')
plt.ylabel(r'Current ($\mu$A)')
plt.title('Current vs. Time (Charge process)')
plt.xlim(0, 50)
plt.ylim(0, 10)
plt.legend()
plt.savefig('snippet-full.eps', format='eps')
plt.show()

# for label, voltage, data, color in dataset:
#     t = data[:, 0]
#     V_discharge = data[:, 2]
#     I_discharge = V_discharge/R2
#     V_charge = data[:, 1]
#     I_charge = V_charge/R2
#     Q_charge = np.abs(np.trapezoid(I_charge, t))
#     Q_discharge = np.abs(np.trapezoid(I_discharge, t))
#     Q_diff = Q_charge - Q_discharge
#     plt.plot(voltage, Q_diff*1e9, 'o', color=color, markersize=8, label=label)

# plt.axhline(y=0.0, color='black', ls='--', lw=1)
# plt.xlabel('Pulse Voltage (V)', fontsize=19)
# plt.ylabel(r'Diff Charge (nC)', fontsize=19)
# plt.title('DLTS Signal vs Time', fontsize=20)
# plt.xlim(-50, 0)
# plt.ylim(0, 10)
# plt.legend(frameon=True, numpoints=1, fontsize=15)
# # plt.savefig('DLTS_pulse-var.eps', format='eps', bbox_inches='tight')
# plt.show()


