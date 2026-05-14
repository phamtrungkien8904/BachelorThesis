# === File & Measurement Info ==============================
MyPythonFile  = "zz154"
#MyDataFile    = "Proj03xxxx.dat"

MyMeasurement = "ChangingV34"
#MyDevice      = "51*51*101 vdP geometry"
#MyQuestion    = "Role of Potential steps"
#MyAnswer      = "Significant change of n2D"

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
Z1 = np.loadtxt('Proj031Poti.dat')   # VG4=-5, V34=0
Z3 = np.loadtxt('Proj033Poti.dat')   # VG4=-5, V34=-2
Z5 = np.loadtxt('Proj035Poti.dat')   # VG4=-5, V34=-4
Z2 = np.loadtxt('Proj031n2D.dat')    # same sequence
Z4 = np.loadtxt('Proj033n2D.dat')   
Z6 = np.loadtxt('Proj035n2D.dat')  

"Data manipulation"
Z2=Z2/1e16
Z4=Z4/1e16
Z6=Z6/1e16

"Line extraction"
Z2Row3n2D= np.take(Z2, indices=2, axis=0)
Z2Col3n2D= np.take(Z2, indices=2, axis=1)
Z4Row3n2D= np.take(Z4, indices=2, axis=0)
Z4Col3n2D= np.take(Z4, indices=2, axis=1)
Z6Row3n2D= np.take(Z6, indices=2, axis=0)
Z6Col3n2D= np.take(Z6, indices=2, axis=1)

xValues = np.linspace(50, 0, 51)
yValues = np.linspace(0, 50, 51)

"Figure: definition, size and resolution"
cmu = 1/2.54                                # centimeters unit in inches
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(30*cmu, 20*cmu))
plt.subplots_adjust(left=0.12,      #left margin
                    bottom=0.1,     #bottom margin 
                    right=0.9,     #right margin 
                    top=0.9,       # top margin
                    wspace=0.5,     # width space
                    hspace=0.3)     # height space
axes[0, 0]
axes[0, 1]
axes[0, 2]
axes[1, 0]
axes[1, 1]
axes[1, 2]
ax1, ax2, ax3, ax4, ax5, ax6 = axes.flatten()

"Figure: data to be plotted:"
im1 = ax1.imshow(Z1, extent=[0, 50, 0, 50], interpolation='nearest')
im2 = ax2.imshow(Z2, extent=[0, 50, 0, 50], interpolation='nearest')
ax3.plot(yValues, Z2Row3n2D,'k', linewidth=1.5, color = 'k', linestyle='--')
ax3.plot(xValues, Z2Col3n2D,'k', linewidth=1.5, color = 'r', linestyle='--')
ax3.set_ylim([0, 3])

im4 = ax4.imshow(Z3, extent=[0, 50, 0, 50], interpolation='nearest')
im5 = ax5.imshow(Z4, extent=[0, 50, 0, 50], interpolation='nearest')
ax6.plot(yValues, Z4Row3n2D,'k', linewidth=1.5, color = 'k', linestyle='--')
ax6.plot(xValues, Z4Col3n2D,'k', linewidth=1.5, color = 'r', linestyle='--')
ax6.set_ylim([0, 3])

"Figure: color bar"
cbar1 = fig.colorbar(im1, ax = ax1)
cbar1.set_label("Potential (V)", loc = 'top')
cbar2 = fig.colorbar(im2, ax = ax2)
cbar2.set_label("$n_{2D}$ ($10^{12}$ cm$^{-2}$)", loc = 'top')
cbar4 = fig.colorbar(im4, ax = ax4)
cbar4.set_label("Potential (V)", loc = 'top')
cbar5 = fig.colorbar(im5, ax = ax5)
cbar5.set_label("$n_{2D}$ ($10^{12}$ cm$^{-2}$)", loc = 'top')

"Figure: labels, ticks, and legend"
ax1.set_ylabel(r"$x$-Position (nm)", fontsize = 10, color = 'k', rotation = 90)
ax1.set_xlabel(r"$y$-Position (nm)", fontsize = 10, color = 'k', rotation =0)
ax2.set_ylabel(r"$x$-Position (nm)", fontsize = 10, color = 'k', rotation = 90)
ax2.set_xlabel(r"$y$-Position (nm)", fontsize = 10, color = 'k', rotation =0)
ax4.set_ylabel(r"$x$-Position (nm)", fontsize = 10, color = 'k', rotation = 90)
ax4.set_xlabel(r"$y$-Position (nm)", fontsize = 10, color = 'k', rotation =0)
ax5.set_ylabel(r"$x$-Position (nm)", fontsize = 10, color = 'k', rotation = 90)
ax5.set_xlabel(r"$y$-Position (nm)", fontsize = 10, color = 'k', rotation = 0)

ax3.set_ylabel(r"$n_{2D}$ ($10^{12}$ cm$^{-2}$)", fontsize = 10, color = 'k', rotation = 90)
ax3.set_xlabel(r"$x/y$-Position (nm)", fontsize = 10, color = 'k', rotation = 0)
ax6.set_ylabel(r"$n_{2D}$ ($10^{12}$ cm$^{-2}$)", fontsize = 10, color = 'k', rotation = 90)
ax6.set_xlabel(r"$x/y$-Position (nm)", fontsize = 10, color = 'k', rotation = 0)

"Vertical lines"
ax2.axvline(x=3, color='r', linewidth=1.5, linestyle='--')
ax2.axhline(y=47, color='k', linewidth=1.5, linestyle='--')
ax5.axvline(x=3, color='r', linewidth=1.5, linestyle='--')
ax5.axhline(y=47, color='k', linewidth=1.5, linestyle='--')

"Annotations"
plt.figtext(0.085, 0.91, r"a) $V_{34} = 0.0$ V and $V_{G4}$ = -5.0 V", color = 'k')
plt.figtext(0.375, 0.91, r"b) $V_{34} = 0.0$ V and $V_{G4}$ = -5.0 V", color = 'k')
plt.figtext(0.705, 0.91, r"c) $V_{34} = 0.0$ V and $V_{G4}$ = -5.0 V", color = 'k')
plt.figtext(0.085, 0.46, r"d) $V_{34} = -2.0$ V and $V_{G4}$ = -5.0 V", color = 'k')
plt.figtext(0.375, 0.46, r"e) $V_{34} = -2.0$ V and $V_{G4}$ = -5.0 V", color = 'k')
plt.figtext(0.705, 0.46, r"f) $V_{34} = -2.0$ V and $V_{G4}$ = -5.0 V", color = 'k')

"Figure: show"
plt.show()

"Saving plots to eps and pdf:"
fig.savefig(MyPythonFile + ".eps", format="eps")
fig.savefig(MyPythonFile + ".pdf", format="pdf")