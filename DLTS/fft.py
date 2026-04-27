from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt

# Custom settings
plt.style.use('classic')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['figure.dpi'] = 100

data = np.loadtxt("./Data/20262704003.dat")

t_min = 0.02
t_max = 0.3

# Keep only samples in the requested time window
time_mask = (data[:, 0] >= t_min) & (data[:, 0] <= t_max)
data = data[time_mask]

f_min = 10.0  # Hz
f_max = 100.0  # Hz

R = 100e3  # Resistance in ohms
C = 2.1e-9  # Capacitance in farads
fc = 1 / (2 * np.pi * R * C)  # Cutoff frequency in Hz
print(f"Cutoff frequency: {fc:.2f} Hz")


# Number of sample points
N = data.shape[0]
# sample spacing
T = data[1, 0] - data[0, 0]

x = data[:, 0]
y_in = data[:, 3]  # V_in
y_out = data[:, 3] - data[:, 1]  # V_C = V_in - V_R


yf_in = fft(y_in)
yf_out = fft(y_out)

# Only keep the positive frequency components for plotting/exporting
half = N // 2
xf = fftfreq(N, T)[:half]
yf_in_half = yf_in[:half]
yf_out_half = yf_out[:half]

# Truncate output once frequencies exceed 2 kHz
mask = xf <= f_max
xf = xf[mask]
yf_in_half = yf_in_half[mask]
yf_out_half = yf_out_half[mask]

amplitude_scale = 2.0 / N
amp_in = amplitude_scale * np.abs(yf_in_half)
amp_out = amplitude_scale * np.abs(yf_out_half)

eps = np.finfo(float).eps
valid = (amp_in > eps) & (amp_out > eps)

# np.savetxt(
# 	"fft.csv",
# 	np.column_stack((xf, amp_in, amp_out)),
# 	delimiter=",",
# 	header="frequency,input_amplitude,output_amplitude",
# 	comments="",
# )

plt.plot(xf, amp_in, label="Input")
plt.plot(xf, amp_out, label="Output")
plt.xlim(f_min, f_max)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (V)")
plt.title("Amplitude Spectrum")
plt.legend()
plt.show()

G = 20*np.log10(amp_out[valid] / amp_in[valid])
plt.semilogx(xf[valid], G, label="Gain (dB)")
plt.xlim(f_min, f_max)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Gain (dB)")
plt.title("Bode Diagram")
plt.legend()
plt.show()
