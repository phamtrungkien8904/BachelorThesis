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
    # 'figure.figsize': (10/2.54, 6/2.54),  # 10x6 cm in inches (1 figure per line)
    'figure.figsize': (8/2.54, 6/2.54),  # 10x6 cm in inches (2 figures per line)
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

data1 = np.loadtxt("./Data-20260705/20260705001.dat")
data2 = np.loadtxt("./Data-20260705/20260705002.dat")
data3 = np.loadtxt("./Data-20260705/20260705003.dat")
data4 = np.loadtxt("./Data-20260705/20260705006.dat")

datasets = [
    ('20', 20e6, data2, 'red', 'o'),
    ('30', 30e6, data1, 'blue', 's'),
    ('40', 40e6, data3, 'green', '^'),
    ('50', 50e6, data4, 'orange', 'D'),
]

for label, R_D, data, color, marker in datasets:
    V_GS = data[:, 0]
    I_D = data[:, 1]
    V_DS = data[:, 2]
    V_out = V_DS - I_D * R_D
    V_in = V_GS
    plt.plot(-V_in, -V_out, linestyle='-', color=color, label=label,markevery=40, marker=marker)
plt.xlabel(r'Input Voltage $-V_\text{in}$ (V)')
plt.ylabel(r'Output Voltage $-V_\text{out}$ (V)')
plt.xlim(0, 40)
plt.ylim(0, 40)
plt.title(r'O-FET Transfer Characteristics ($V_\text{DD} = -30$ V)')
plt.legend(title = r'$R_D$ (M$\Omega$)',loc='upper right')
plt.savefig("oFET-transfer.eps", format='eps')
plt.show()

for label, R_D, data, color, marker in datasets:
    V_GS = data[:, 0]
    I_D = data[:, 1]
    V_DS = data[:, 2]
    V_out = V_DS - I_D * R_D
    V_in = V_GS
    A = np.diff(V_out) / np.diff(V_in)

    window_size = 20
    window = np.ones(window_size) / window_size

    V_in_smooth = np.convolve(V_in, window, mode='same')
    A_smooth = np.convolve(A, window, mode='same')
    plt.plot(-V_in_smooth[15:-10], A_smooth[15:-9],  color=color, label=label, marker=marker, markevery=40)
plt.xlabel(r'Input Voltage $-V_\text{in}$ (V)')
plt.ylabel(r'Amplification $A$')
plt.xlim(0, 40)
plt.title(r'O-FET Amplification Characteristics ($V_\text{DD} = -30$ V)')
plt.legend(title = r'$R_D$ (M$\Omega$)', loc='lower right')
plt.savefig("oFET-amp.eps", format='eps')
plt.show()