# === File & Measurement Info ==============================
MyPythonFile  = "zz153"
MyMeasurement = "ChangingV34"

"Imports"
import matplotlib.pyplot as plt
import numpy as np

"Restore defaults"
plt.rcdefaults()

"More general settings"
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.top'] = True
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

"LaTeX related"
plt.rcParams["font.family"]='sans-serif'

"Load data"
P1 = np.loadtxt('Proj021Poti.dat')    
P2 = np.loadtxt('Proj022Poti.dat')    
P3 = np.loadtxt('Proj023Poti.dat')    
P4 = np.loadtxt('Proj024Poti.dat')    
P5 = np.loadtxt('Proj025Poti.dat')    
P6 = np.loadtxt('Proj026Poti.dat')    

"Data manipulation, line extraction"
P1Row3= np.take(P1, indices=2, axis=0)
P1Row25= np.take(P1, indices=25, axis=0)
P2Row3= np.take(P2, indices=2, axis=0)
P2Row25= np.take(P2, indices=25, axis=0)
P3Row3= np.take(P3, indices=2, axis=0)
P3Row25= np.take(P3, indices=25, axis=0)
P4Row3= np.take(P4, indices=2, axis=0)
P4Row25= np.take(P4, indices=25, axis=0)
P5Row3= np.take(P5, indices=2, axis=0)
P5Row25= np.take(P5, indices=25, axis=0)

"Generate x-axis"
xValues = np.linspace(0, 50, 51)

# === Figure ===============================================
"Figure: definition, size and resolution"
cmu = 1/2.54                                # centimeters unit in inches
fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(10*cmu, 8*cmu))
plt.subplots_adjust(left=0.13,      #left margin
                    bottom=0.13,     #bottom margin 
                    right=0.9,     #right margin 
                    top=0.9,       # top margin
                    wspace=0.3,     # width space
                    hspace=0.1)     # height space

ax1.set_xlabel(r"$x$ (nm)")
ax1.set_ylabel("$\\phi$ (V)")

# === Plots ===============================================
ax1.plot(xValues, P1Row3, linewidth=0.7, color='k', label=r"$V_{34}= 0.0$ V")
ax1.plot(xValues, P5Row3, linewidth=0.7, color='r', label= r"$V_{34}= -4.0$ V")

ax1.legend()

# === Annotations =========================================
fig.text(0.15, 0.4, r"$V_{G4} = -5.0$")

# === Show & Save =========================================
plt.show()

fig.savefig(MyPythonFile + ".eps", format="eps")
fig.savefig(MyPythonFile + ".pdf", format="pdf")