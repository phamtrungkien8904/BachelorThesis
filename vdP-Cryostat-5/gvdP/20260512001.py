# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 17:27:31 2026

@author: VP
"""

# === File Information =====================================
MyFileName   = "20260512001"
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
plt.rcParams["font.family"]      = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["figure.dpi"]       = 300
plt.rcParams['xtick.direction']  = 'in'
plt.rcParams['ytick.direction']  = 'in'
plt.rcParams['xtick.top']        = True
plt.rcParams['ytick.right']      = True

"""
Column format:
0: VG4 (V)
1: IG4 (A)
2: I34 (V)
3: V34 (A)
4: V14 (V)
5: V24 (V)
6: V12 (V)
7: Cond34 (1/Ohm)
5: n2D
9: Mobility
"""

# ============================================================
# Load Data
# ============================================================
Data1 = np.loadtxt("./" + MyDataFile1)
Data2 = np.loadtxt("./" + MyDataFile2)
Data3 = np.loadtxt("./" + MyDataFile3)

# ============================================================
# Apply V34 limit (|V34| ≤ 25 V)
# ============================================================

VG4_1 = Data1[:,0]
mob_1 = Data1[:,9]

VG4_2 = Data2[:,0]
mob_2 = Data2[:,9]

VG4_3 = Data3[:,0]
mob_3 = Data3[:,9]
# ============================================================
# Convert cm → inches
# ============================================================
cm = 1.0 / 2.54

# ============================================================
# Create Figure
# ============================================================
fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(12*cm, 10*cm))
plt.subplots_adjust(left=0.18, bottom=0.18, right=0.97, top=0.72)

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

ax1.set_xlabel(r"$-V_{G4}$ (V)")
ax1.set_ylabel(r"$\mu$ (cm$^2$/Vs)")
ax1.set_xlim([-51,1])          # adjust if needed
ax1.set_ylim([-0.1,6.1])  # optional manual limits

ax1.tick_params(labelsize=10)
ax1.legend(fontsize=8, frameon=False)

# ============================================================
# Figure Text
# ============================================================
fig.suptitle(MyDescription, fontsize=12)

plt.figtext(0.12, 0.90, "FileName: " + MyFileName, fontsize=8)
plt.figtext(0.80, 0.90, "Date: " + MyExpDate, fontsize=8)
plt.figtext(0.12, 0.87, "Python: " + MyPython, fontsize=8)
plt.figtext(0.12, 0.84, "Sample: " + MySampleName, fontsize=8)
plt.figtext(0.12, 0.81, "Data: " +
            MyDataFile1 + ", " +
            MyDataFile2 + ", " +
            MyDataFile3, fontsize=8)
plt.figtext(0.12, 0.78, "Parameters: " + Parameters, fontsize=8)

# ============================================================
# Show and Save
# ============================================================
plt.show()

fig.savefig(MyFileName + ".eps", format="eps")
fig.savefig(MyFileName + ".pdf", format="pdf")
fig.savefig(MyFileName + ".png", format="png")
fig.savefig(MyFileName + ".jpeg", format="jpeg")