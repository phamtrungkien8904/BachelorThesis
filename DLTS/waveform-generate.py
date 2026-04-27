import numpy as np
import matplotlib.pyplot as plt

sample_rate = 10000  # samples per second
t_start = 0.02  # seconds
t_end = 0.42  # seconds

start = int(t_start * sample_rate) # samples
end = int(t_end * sample_rate) # samples

A = 3.0 # amplitude in volts
# f = 10/sample_rate # 10 Hz

# with open("waveform.wfm", "w") as f_out:
#     for t in range(start, end + 1):
#         v = A * np.sin(2 * np.pi * f * (t - start))
#         f_out.write(f"{t}\t{v:.6f}\t0\t0\t0\n")

# AC sweep
f0 = 10/sample_rate   # 10 Hz
f1 = 2000/sample_rate  # 1000 Hz
df = 5/sample_rate  # frequency step of 10 Hz

# Build stepped frequencies in normalized units (cycles per sample)
freqs = np.arange(f0, f1 + 0.5 * df, df)
N = end - start + 1
samples_per_step = max(1, N // len(freqs))

with open("waveform.wfm", "w") as f_out:
    phase = 0.0
    for t in range(start, end + 1):
        n = t - start
        step_idx = min(n // samples_per_step, len(freqs) - 1)
        f = freqs[step_idx]
        phase += 2 * np.pi * f
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
