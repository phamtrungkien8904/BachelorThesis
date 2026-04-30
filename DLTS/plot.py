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

t = np.linspace(0, 0.05, 500)  # Time array from 0 to 50 ms


def charge_curve(t, a_fast=1.85, tau_fast=4.0e-4, a_slow=0.45, tau_slow=1.2e-2, beta=0.78, baseline=0.0):
    """Empirical charge relaxation with a fast initial recovery and a slow tail."""
    return baseline - a_fast * np.exp(-t / tau_fast) - a_slow * np.exp(-(t / tau_slow) ** beta)


def func(t):
    return charge_curve(t)


if __name__ == '__main__':
    plt.plot(t * 1e3, charge_curve(t), label='Charge relaxation model', color='blue', lw=2, linestyle='--')
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage signal (V)')
    plt.xlim(0.00, 50)
    plt.ylim(-2.6, 0.2)
    plt.legend()
    plt.show()