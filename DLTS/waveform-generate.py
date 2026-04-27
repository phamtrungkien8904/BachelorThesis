import numpy as np
import matplotlib.pyplot as plt

sample_rate = 10000  # samples per second
start = int(0.02*sample_rate) # seconds
end = int(0.3*sample_rate) # seconds

A = 5.0 # amplitude in volts
# f = 10/sample_rate # 10 Hz

# with open("waveform.wfm", "w") as f_out:
#     for t in range(start, end + 1):
#         v = A * np.sin(2 * np.pi * f * (t - start))
#         f_out.write(f"{t}\t{v:.6f}\t0\t0\t0\n")

# AC sweep
f0 = 10/sample_rate   # 10 Hz
f1 = 100/sample_rate  # 100 Hz

T = end - start  # total duration (in your time units)

with open("waveform.wfm", "w") as f_out:
    for t in range(start, end + 1):
        tau = t - start  # normalized time starting at 0
        # phase for linear chirp
        phase = 2 * np.pi * (
            f0 * tau +
            0.5 * (f1 - f0) * (tau ** 2) / T
        )
        v = A * np.sin(phase)
        f_out.write(f"{t}\t{v:.6f}\t0\t0\t0\n")

data = np.loadtxt("waveform.wfm")
plt.plot(data[:, 0], data[:, 1])
plt.xlim(start, end)
plt.ylim(-5, 5)
plt.xlabel("Sample Index")
plt.ylabel("Voltage (V)")
plt.title("Generated Sine Wave")
# plt.grid()
plt.show()
