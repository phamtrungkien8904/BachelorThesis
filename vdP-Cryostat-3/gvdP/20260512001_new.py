# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 17:27:31 2026

@author: VP
"""

# === File Information =====================================
MyFileName   = "20260512001_publishable"
MyExpDate    = "12.05.2026"
MySampleName = "PaN [20250505_5] , PS [20260505_1]  , TripC12 [20260505_4]"
MyPython     = "20260512001.py"

MyDataFile1  = "20260512005.dat"   # PaN
MyDataFile2  = "20260512003.dat"   # PS
MyDataFile3  = "20260512004.dat"   # Trip_C12

MyDescription = "Mobility vs VG4"
Parameters = "I34 = 100 nA,  V34(lim) = 20 V"

# ============================================================
# Imports
# ============================================================
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# Restore Defaults
# ============================================================
plt.rcdefaults()
plt.rcParams["font.family"]      = "sans serif"
plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["figure.dpi"]       = 300
plt.rcParams["xtick.direction"]  = "in"
plt.rcParams["ytick.direction"]  = "in"
plt.rcParams["xtick.top"]        = True
plt.rcParams["ytick.right"]      = True

"""
Column format:
0: VG4 (V)
1: IG4 (A)
2: I34
3: V34
4: V14 (V)
5: V24 (V)
6: V12 (V)
7: Cond34 (1/Ohm)
8: n2D
9: Mobility
"""

# ============================================================
# Physical Constants / Device Parameters
# ============================================================
Charge = 1.602e-19
DevArea = 32e-6

C_PaN  = 2.1e-9
C_PS   = 1.9e-9
C_Trip = 1.9e-9

# ============================================================
# Load Data
# ============================================================
Data1 = np.loadtxt("./" + MyDataFile1)   # PaN
Data2 = np.loadtxt("./" + MyDataFile2)   # PS
Data3 = np.loadtxt("./" + MyDataFile3)   # Trip_C12

# ============================================================
# Mobility Calculation
# ============================================================
def calculate_n2d_and_mu(data, devcap, area=DevArea, charge=Charge):
    vg4 = data[:, 0]
    i34 = data[:, 2]
    v12 = -data[:, 6]

    sigma2d = 0.22 * (i34 / v12)
    n2d = (devcap * np.abs(vg4)) / (area * charge * 1e4)
    mu = sigma2d / (charge * n2d)

    return vg4, n2d, mu, sigma2d

def get_value_at_vg4(data_x, data_y, vg_target=-50.0):
    idx = np.argmin(np.abs(data_x - vg_target))
    return data_x[idx], data_y[idx]

# ============================================================
# Calculate for all samples
# ============================================================
VG4_1, n2d_1, mob_1, sigma2d_1 = calculate_n2d_and_mu(Data1, C_PaN)
VG4_2, n2d_2, mob_2, sigma2d_2 = calculate_n2d_and_mu(Data2, C_PS)
VG4_3, n2d_3, mob_3, sigma2d_3 = calculate_n2d_and_mu(Data3, C_Trip)

vg_pan_m50,  n2d_pan_m50  = get_value_at_vg4(VG4_1, n2d_1, -50.0)
vg_ps_m50,   n2d_ps_m50   = get_value_at_vg4(VG4_2, n2d_2, -50.0)
vg_trip_m50, n2d_trip_m50 = get_value_at_vg4(VG4_3, n2d_3, -50.0)

vg_pan_mu,  mu_pan_m50  = get_value_at_vg4(VG4_1, mob_1, -50.0)
vg_ps_mu,   mu_ps_m50   = get_value_at_vg4(VG4_2, mob_2, -50.0)
vg_trip_mu, mu_trip_m50 = get_value_at_vg4(VG4_3, mob_3, -50.0)

print(f"PaN: VG4 = {vg_pan_m50:.2f} V, n2D = {n2d_pan_m50:.3e} cm^-2, mu = {mu_pan_m50:.3e} cm^2/Vs")
print(f"PS: VG4 = {vg_ps_m50:.2f} V, n2D = {n2d_ps_m50:.3e} cm^-2, mu = {mu_ps_m50:.3e} cm^2/Vs")
print(f"Trip_C12: VG4 = {vg_trip_m50:.2f} V, n2D = {n2d_trip_m50:.3e} cm^-2, mu = {mu_trip_m50:.3e} cm^2/Vs")

# ============================================================
# Convert cm → inches
# ============================================================
cm = 1.0 / 2.54

# ============================================================
# Create Figure
# ============================================================
fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(12 * cm, 8 * cm))
plt.subplots_adjust(left=0.10, bottom=0.12, right=0.96, top=0.96)

# Styling
colors     = ['k', 'r', 'b']
markers    = ['o', 's', '^']
linestyles = ['solid', 'solid', 'solid']

labels = [
    "PaN",
    "PS",
    "Trip_C12"
]

# ============================================================
# Plot Mobility
# ============================================================
ax1.plot(VG4_1, mob_1,
         color=colors[0], linestyle=linestyles[0],
         marker=markers[0], markersize=2,
         linewidth=0.8, label=labels[0], markevery=10)

ax1.plot(VG4_2, mob_2,
         color=colors[1], linestyle=linestyles[1],
         marker=markers[1], markersize=2,
         linewidth=0.8, label=labels[1], markevery=10)

ax1.plot(VG4_3, mob_3,
         color=colors[2], linestyle=linestyles[2],
         marker=markers[2], markersize=2,
         linewidth=0.8, label=labels[2], markevery=10)

ax1.set_xlabel(r"$-V_{G4}$ (V)", fontsize=8)
ax1.set_ylabel(r"$\mu$ (cm$^2$/Vs)", fontsize=8)
ax1.set_xlim([-50, -5])
ax1.set_ylim([0, 6])

ax1.tick_params(labelsize=8)
ax1.legend(fontsize=8, frameon=False)

# ============================================================
# Figure Text
# ============================================================
#fig.suptitle(MyDescription, fontsize=12)

#plt.figtext(0.12, 0.90, "FileName: " + MyFileName, fontsize=8)
#plt.figtext(0.80, 0.90, "Date: " + MyExpDate, fontsize=8)
#plt.figtext(0.12, 0.87, "Python: " + MyPython, fontsize=8)
#plt.figtext(0.12, 0.84, "Sample: " + MySampleName, fontsize=8)
#plt.figtext(0.12, 0.81, "Data: " +
#            MyDataFile1 + ", " +
#            MyDataFile2 + ", " +
#            MyDataFile3, fontsize=8)
#plt.figtext(0.12, 0.78, "Parameters: " + Parameters, fontsize=8)

# ============================================================
# Show and Save
# ============================================================
fig.savefig(MyFileName + ".eps", format="eps")
fig.savefig(MyFileName + ".pdf", format="pdf")
fig.savefig(MyFileName + ".png", format="png")
fig.savefig(MyFileName + ".jpeg", format="jpeg")
plt.show()