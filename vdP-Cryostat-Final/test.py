import numpy as np
import matplotlib.pyplot as plt


a = 10
a_var = np.ones(50) * a
x = np.linspace(0, 10, 50)
ratio = 0.1
a_error = np.random.uniform(a*(1-ratio), a*(1+ratio), 50)


plt.scatter(x, a_error, color='red', marker='o')
plt.axhline(a, color='red', ls='--')
plt.ylim(0, 20)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Simple Plot")
plt.show()
