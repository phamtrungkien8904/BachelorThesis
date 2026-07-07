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
data = np.loadtxt('Data-20260805/20260508-0001.csv', delimiter=',', skiprows=1)
time = data[:, 0]
V_in = data[:, 1]
V_out = data[:, 2]

window_size = 5
window = np.ones(window_size) / window_size

V_in_smooth = np.convolve(V_in, window, mode='same')
V_out_smooth = np.convolve(V_out, window, mode='same')

plt.plot(time*1e-3, -V_in_smooth, label='Input Signal', color='blue')
plt.plot(time*1e-3, V_out_smooth, label='Output Signal', color='red')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.xlim(-0.3, 0.3)
plt.ylim(-2, 2)
plt.title(
    r'O-FET Amplifier Response'
    '\n'
    r'($V_\text{DD} = -30$ V, $R_D = 50$ M$\Omega$, $f = 10$ kHz)',
)
plt.legend()
plt.savefig("amp-response-sin.eps", format='eps')
plt.show()

data = np.loadtxt('Data-20260805/20260508-0002.csv', delimiter=',', skiprows=1)
time = data[:, 0]
V_in = data[:, 1]
V_out = data[:, 2]

window_size = 5
window = np.ones(window_size) / window_size

V_in_smooth = np.convolve(V_in, window, mode='same')
V_out_smooth = np.convolve(V_out, window, mode='same')

plt.plot(time*1e-3, -V_in_smooth, label='Input Signal', color='blue')
plt.plot(time*1e-3, V_out_smooth, label='Output Signal', color='red')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.xlim(-0.3, 0.3)
plt.ylim(-2, 2)
plt.title(
    r'O-FET Amplifier Response'
    '\n'
    r'($V_\text{DD} = -30$ V, $R_D = 50$ M$\Omega$, $f = 10$ kHz)',
)
plt.legend()
plt.savefig("amp-response-square.eps", format='eps')
plt.show()