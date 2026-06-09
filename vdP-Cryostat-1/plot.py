import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(1, 100, 100)
y = np.exp(-10000/x)


plt.semilogy(x,y)

plt.show()