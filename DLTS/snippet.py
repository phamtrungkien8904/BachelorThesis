import numpy as np
import matplotlib.pyplot as plt

# # Custom settings
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

data1 = np.loadtxt("./Data_20262904/20262904005.snp") # 40V
data2 = np.loadtxt("./Data_20262904/20262904004.snp") # 35V
data3 = np.loadtxt("./Data_20262904/20262904001.snp") # 30V
data4 = np.loadtxt("./Data_20262904/20262904002.snp") # 25V
data5 = np.loadtxt("./Data_20262904/20262904003.snp") # 20V
data6 = np.loadtxt("./Data_20262904/20262904006.snp") # 15V
data7 = np.loadtxt("./Data_20262904/20262904007.snp") # 10V

dataset = [
    ("-40 V", -40, data1, 'red'),
    ("-35 V", -35, data2, 'orange'),
    ("-30 V", -30, data3, 'green'),
    ("-25 V", -25, data4, 'blue'),
    ("-20 V", -20, data5, 'purple'),
    ("-15 V", -15, data6, 'brown'),
    ("-10 V", -10, data7, 'cyan')
]

R1 = 1e6  # 1 MΩ
R2 = 1e5 # 1 MΩ

t = data1[:, 0]
V_discharge = data1[:, 2]
V_charge = data1[:, 1]
I_discharge = V_discharge/R2
I_charge = V_charge/R2
Q_charge = np.abs(np.trapezoid(I_charge, t))
Q_discharge = np.abs(np.trapezoid(I_discharge, t))
Q_diff = Q_charge - Q_discharge
q_text = (
    f"Charge Q: {Q_charge*1e9:.2f} nC\n"
    f"Discharge Q: {Q_discharge*1e9:.2f} nC\n"
    f"Difference Q: {Q_diff*1e9:.2f} nC"
)

plt.plot(t*1e3, I_discharge*1e6, label='Discharge Current', color='red', ls='-', lw = 1.5)
plt.plot(t*1e3, I_charge*1e6, label='Charge Current', color='blue', ls='-', lw = 1.5)
plt.axhline(y=0.0, color='black', ls='--', lw=1)
plt.xlabel('Time (ms)', fontsize=19)
plt.ylabel(r'Current ($\mu$A)', fontsize=19)
plt.title('DLTS Signal vs Time', fontsize=20)
plt.text(
    0.98,
    0.02,
    q_text,
    transform=plt.gca().transAxes,
    fontsize=12,
    va='bottom',
    ha='right',
    bbox=dict(facecolor='white', edgecolor='black', alpha=0.85)
)
# plt.xlim(0, 50)
# plt.ylim(0, 10)
plt.legend(frameon=True, numpoints=1, fontsize=15)
# plt.savefig('snippet.eps', format='eps', bbox_inches='tight')
plt.show()