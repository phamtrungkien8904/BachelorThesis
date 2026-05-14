import numpy as np
import matplotlib.pyplot as plt

File_index_1 = "04"
File_index_2 = "05"
File_index_3 = "06"

data_Poti_1 = np.loadtxt(f"./Data/Data_Poti_{File_index_1}.dat")
data_Poti_2 = np.loadtxt(f"./Data/Data_Poti_{File_index_2}.dat")
data_n2D_1 = np.loadtxt(f"./Data/Data_n2D_{File_index_1}.dat")
data_n2D_2 = np.loadtxt(f"./Data/Data_n2D_{File_index_2}.dat")
data_error_1 = np.loadtxt(f"./Data/Data_Error_{File_index_1}.dat")
data_error_2 = np.loadtxt(f"./Data/Data_Error_{File_index_2}.dat")
data_Poti_3 = np.loadtxt(f"./Data/Data_Poti_{File_index_3}.dat")
data_n2D_3 = np.loadtxt(f"./Data/Data_n2D_{File_index_3}.dat")


error_index = np.arange(1, len(data_error_1) + 1)



N = 101
L = 50  # Physical size of the domain in nm
x = np.linspace(0, L, N)
y = np.linspace(0, L, N)
X, Y = np.meshgrid(x, y)

V_1 = data_Poti_1
V_2 = data_Poti_2
V_3 = data_Poti_3
p_1 = data_n2D_1
p_2 = data_n2D_2
p_3 = data_n2D_3

# File 1
fig1 = plt.figure(figsize=(14, 6), constrained_layout=True)
gs1 = fig1.add_gridspec(1, 2, width_ratios=[1, 1.05])

ax_n2d_1 = fig1.add_subplot(gs1[0, 1])
image_n2d_1 = ax_n2d_1.imshow(
    p_1,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='viridis',
    interpolation='bicubic',
    vmin=0,
    vmax=p_3.max()
)
fig1.colorbar(image_n2d_1, ax=ax_n2d_1, shrink=0.9)
ax_n2d_1.set_xlabel('X-Position [nm]')
ax_n2d_1.set_ylabel('Y-Position [nm]')
ax_n2d_1.set_aspect('equal')
ax_n2d_1.set_xlim(0, L)
ax_n2d_1.set_ylim(0, L)
ax_n2d_1.set_title('2D Charge Density Distribution')

ax_pot_1 = fig1.add_subplot(gs1[0, 0])
image_pot_1 = ax_pot_1.imshow(
    V_1,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='jet',
    interpolation='bicubic',
        vmin=V_3.min(),
        vmax=0
)
fig1.colorbar(image_pot_1, ax=ax_pot_1, shrink=0.9)
ax_pot_1.set_xlabel('X-Position [nm]')
ax_pot_1.set_ylabel('Y-Position [nm]')
ax_pot_1.set_aspect('equal')
ax_pot_1.set_xlim(0, L)
ax_pot_1.set_ylim(0, L)
ax_pot_1.set_title('2D Potential Distribution')
fig1.suptitle('File 01: Charge Density and Potential Distribution (V34 = 0 V)')
plt.savefig(f"./Figures/Plot_{File_index_1}.eps", format='eps', bbox_inches='tight')  # Save the figure with high resolution
plt.show()

# File 2
fig2 = plt.figure(figsize=(14, 6), constrained_layout=True)
gs2 = fig2.add_gridspec(1, 2, width_ratios=[1, 1.05])

ax_n2d_2 = fig2.add_subplot(gs2[0, 1])
image_n2d_2 = ax_n2d_2.imshow(
    p_2,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='viridis',
    interpolation='bicubic',
    vmin=0,
    vmax=p_3.max()
)
fig2.colorbar(image_n2d_2, ax=ax_n2d_2, shrink=0.9)
ax_n2d_2.set_xlabel('X-Position [nm]')
ax_n2d_2.set_ylabel('Y-Position [nm]')
ax_n2d_2.set_aspect('equal')
ax_n2d_2.set_xlim(0, L)
ax_n2d_2.set_ylim(0, L)
ax_n2d_2.set_title('2D Charge Density Distribution')

ax_pot_2 = fig2.add_subplot(gs2[0, 0])
image_pot_2 = ax_pot_2.imshow(
    V_2,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='jet',
    interpolation='bicubic',
    vmin=V_3.min(),
    vmax=0
)
fig2.colorbar(image_pot_2, ax=ax_pot_2, shrink=0.9)
ax_pot_2.set_xlabel('X-Position [nm]')
ax_pot_2.set_ylabel('Y-Position [nm]')
ax_pot_2.set_aspect('equal')
ax_pot_2.set_xlim(0, L)
ax_pot_2.set_ylim(0, L)
ax_pot_2.set_title('2D Potential Distribution')
fig2.suptitle('File 02: Charge Density and Potential Distribution (V34 = -1 V)')

plt.savefig(f"./Figures/Plot_{File_index_2}.eps", format='eps', bbox_inches='tight')  # Save the figure with high resolution
plt.show()

# File 3
fig3 = plt.figure(figsize=(14, 6), constrained_layout=True)
gs3 = fig3.add_gridspec(1, 2, width_ratios=[1, 1.05])

ax_n2d_3 = fig3.add_subplot(gs3[0, 1])
image_n2d_3 = ax_n2d_3.imshow(
    p_3,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='viridis',
    interpolation='bicubic',
    vmin=0,
    vmax=p_3.max()
)
fig3.colorbar(image_n2d_3, ax=ax_n2d_3, shrink=0.9)
ax_n2d_3.set_xlabel('X-Position [nm]')
ax_n2d_3.set_ylabel('Y-Position [nm]')
ax_n2d_3.set_aspect('equal')
ax_n2d_3.set_xlim(0, L)
ax_n2d_3.set_ylim(0, L)
ax_n2d_3.set_title('2D Charge Density Distribution')

ax_pot_3 = fig3.add_subplot(gs3[0, 0])
image_pot_3 = ax_pot_3.imshow(
    V_3,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='jet',
    interpolation='bicubic',
    vmin=V_3.min(),
    vmax=0
)
fig3.colorbar(image_pot_3, ax=ax_pot_3, shrink=0.9)
ax_pot_3.set_xlabel('X-Position [nm]')
ax_pot_3.set_ylabel('Y-Position [nm]')
ax_pot_3.set_aspect('equal')
ax_pot_3.set_xlim(0, L)
ax_pot_3.set_ylim(0, L)
ax_pot_3.set_title('2D Potential Distribution')
fig3.suptitle('File 03: Charge Density and Potential Distribution (V34 = -3 V)')
plt.savefig(f"./Figures/Plot_{File_index_3}.eps", format='eps', bbox_inches='tight')  # Save the figure with high resolution
plt.show()

# 1D line curves along one side of the grid (bottom edge, index 0)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(y, p_1[:, 0], 'b-', linewidth=2)
ax1.plot(y, p_2[:, 0], 'k-', linewidth=2)
ax1.plot(y, p_3[:, 0], 'r-', linewidth=2)
ax1.set_title('Charge Density Profile along 1 side')
ax1.set_xlabel('Position (y) [nm]')
ax1.set_ylabel('Density (p)')

ax2.plot(y, V_1[:, 0], 'b-', linewidth=2)
ax2.plot(y, V_2[:, 0], 'k-', linewidth=2)
ax2.plot(y, V_3[:, 0], 'r-', linewidth=2)
ax2.set_title('Potential Profile along 1 side')
ax2.set_xlabel('Position (y) [nm]')
ax2.set_ylabel('Potential (V)')
plt.savefig(f"./Figures/Plot_1D_vdP.eps", format='eps', bbox_inches='tight')  # Save the figure with high resolution
plt.tight_layout()
plt.show()


plt.plot(error_index, data_error_1)
plt.yscale("log")
plt.xlabel("Iteration")
plt.ylabel("Error (log scale)")
plt.title("Convergence of Poisson Solver")
plt.grid()
plt.show()
