import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('test.dat')
print(data[:,0])

data[:,0] *= 2
print(data[:,0])

np.savetxt('test_mod.dat', data, fmt='%g')