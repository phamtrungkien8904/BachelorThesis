import numpy as np
import matplotlib.pyplot as plt

data1 = np.loadtxt("./Data_KP_IDS_VDS/20261504001.dat")
data2 = np.loadtxt("./Data_KP_IDS_VDS/20261504002.dat")
data3 = np.loadtxt("./Data_KP_IDS_VDS/20261504003.dat")

datasets = [
    ("5 V", data1, 'red'),
    ("2 V", data2, 'blue'),
    ("8 V", data3, 'green'),
]

for label, data, color in datasets:
    V_DS = data[:, 0]
    I_DS = data[:, 1]
    plt.plot(V_DS, I_DS, lw=2, label=label, color=color)

plt.xlabel("V_DS (V)")
plt.ylabel("I_DS (A)")
plt.title("Output Characteristics of MOSFET")
plt.legend()
plt.show()