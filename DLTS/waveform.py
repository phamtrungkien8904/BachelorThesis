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


data1 = np.loadtxt("./Data_20262904/20262904005.dat") # 40V
data2 = np.loadtxt("./Data_20262904/20262904004.dat") # 35V
data3 = np.loadtxt("./Data_20262904/20262904001.dat") # 30V
data4 = np.loadtxt("./Data_20262904/20262904002.dat") # 25V
data5 = np.loadtxt("./Data_20262904/20262904003.dat") # 20V
data6 = np.loadtxt("./Data_20262904/20262904006.dat") # 15V
data7 = np.loadtxt("./Data_20262904/20262904007.dat") # 10V

dataset = [
    ("-40 V", -40, data1, 'red'),
    ("-35 V", -35, data2, 'orange'),
    ("-30 V", -30, data3, 'green'),
    ("-25 V", -25, data4, 'blue'),
    ("-20 V", -20, data5, 'purple'),
    ("-15 V", -15, data6, 'brown'),
    ("-10 V", -10, data7, 'cyan')
]

R1 = 1e6
R2 = 1e5  
Amp = 20

t = data1[:, 0]
V_R = data1[:, 1]
main_trigger = data1[:, 2]
V_in = data1[:, 3]*(-Amp)
second_trigger = data1[:, 4]
I = data1[:, 5]


plt.plot(t, V_in, label='Input Voltage', color = 'orange')
plt.plot(t, V_R*10, label='Current', color = 'k')
# plt.plot(t, main_trigger, label='Main Trigger', lw = 1.5, color = 'red')
# plt.plot(t, second_trigger, label='Second Trigger', lw = 1.5, color = 'black')
plt.xlabel('Time (s)')
plt.ylabel('Signal (arb. units)')
plt.ylim(-50, 50)

plt.title('Signals vs. Time')
plt.legend()
plt.savefig('DLTS-waveform.eps', format='eps')
plt.show()