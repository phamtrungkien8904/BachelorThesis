import numpy as np
import matplotlib.pyplot as plt

# # Custom settings
plt.style.use('classic')
plt.rcParams.update({
    'figure.figsize': (6, 6),
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


plt.figure(figsize=(8, 8))
plt.plot(t, V_in, label='Input Voltage', lw = 2, color = 'orange')
plt.plot(t, V_R*10, label='Gate Current', lw = 2, color = 'k')
# plt.plot(t, main_trigger, label='Main Trigger', lw = 1.5, color = 'red')
# plt.plot(t, second_trigger, label='Second Trigger', lw = 1.5, color = 'black')
plt.xlabel('Time (s)', fontsize=19)
plt.ylabel('Signal (arb. units)', fontsize=19)


plt.title('Signals vs Time', fontsize=20)
plt.legend(frameon=True, numpoints=1, fontsize=15)
# plt.savefig('DLTS.eps', format='eps', bbox_inches='tight')
plt.show()