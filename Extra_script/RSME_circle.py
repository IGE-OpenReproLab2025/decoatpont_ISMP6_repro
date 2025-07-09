import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import imageio.v2 as imageio
import os
from matplotlib.colors import ListedColormap
import xskillscore as xs

#------------------------------------------------ RMSE ON A CIRCLE   ----------------------------------------------------------------------
# AUTHOR: Marine de Coatpont
# April 29, 2025
# IGE / ISMIP6 internship
#
# This script defines a target circle and computes the RMSE between this target and a growing circle over time.
#
# PLEASE READ README (README_SCRIPT.md) FOR MORE INFORMATION ON THIS SCRIPT
#------------------------------------------------------------------------------------------------------------------------------------------

# Parameters
size = 100 
n_times = 100  
max_radius = size // 2
output_dir = "circle_growth_rmse"
gif_name = "circle_growth_rmse.gif"
nc_filename = "circle_data_rmse.nc"
combined_output_dir = "combined_frames_rmse"
combined_gif_name = "combined_circle_rmse.gif"

# Create output directories
os.makedirs(output_dir, exist_ok=True)
os.makedirs(combined_output_dir, exist_ok=True)

# Spatial grid definition
x = np.arange(size)
y = np.arange(size)
X, Y = np.meshgrid(x, y)
center = (size // 2, size // 2)

# Create empty data array
data = np.empty((n_times, size, size))
data[:] = 0

# Define the target circle at t = 50
radius_target = max_radius * 50 / (n_times - 1)
mask_target = (X - center[0])**2 + (Y - center[1])**2 <= radius_target**2
frame_target = np.full((size, size), 0)
frame_target[mask_target] = 1

# Define color maps
color_target = ListedColormap(['white', 'mediumorchid'])
color = ListedColormap(['white', 'mediumpurple'])

# Generate growing circle and save as images
for t in range(n_times):
    radius = max_radius * t / (n_times - 1)
    mask = (X - center[0])**2 + (Y - center[1])**2 <= radius**2
    frame = np.full((size, size), 0)
    frame[mask] = 1
    data[t] = frame

    plt.figure(figsize=(5, 5))
    plt.imshow(frame, origin='lower', cmap=color)
    plt.imshow(frame_target, origin='lower', cmap=color_target, alpha=0.5)
    plt.title(f'Time t = {t}')
    plt.axis('off')
    plt.colorbar(label='Value')
    plt.savefig(f"{output_dir}/frame_{t:03d}.png", bbox_inches='tight')
    plt.close()

# Save data in NetCDF format
ds = xr.Dataset(
    {
        "circle": (("time", "y", "x"), data)
    },
    coords={
        "time": np.arange(n_times),
        "x": x,
        "y": y
    }
)
ds.to_netcdf(nc_filename)
print('NetCDF saved')

# Create GIF of circle evolution
images = []
for t in range(n_times):
    filename = f"{output_dir}/frame_{t:03d}.png"
    images.append(imageio.imread(filename))
imageio.mimsave(gif_name, images, duration=0.2)
print("GIF created")

# Compute RMSE between target and all frames
data_set = xr.open_dataset(nc_filename)
data = data_set.circle
t_target = 50
target_point = data[t_target, :, :]
rmse = []

for t in range(n_times):
    other_points = data[t, :, :]
    distance = xs.rmse(target_point, other_points)
    print('rmse :', distance.values)
    rmse.append(distance.values)

# Plot RMSE over time
plt.figure(figsize=(8, 4))
plt.plot(np.arange(n_times), rmse, color='rebeccapurple')
plt.title(f"RMSE relative to time {t_target}")
plt.xlabel("Time")
plt.ylabel("RMSE")
plt.grid(True)
plt.tight_layout()
plt.savefig("rmse_cercle.png")
print("Figure saved")

# Create combined plot: RMSE + circle at each time step
for t in range(n_times):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].plot(np.arange(t + 1), rmse[:t + 1], color='rebeccapurple', marker='o')
    axs[0].set_xlim(0, n_times - 1)
    axs[0].set_title("RMSE")
    axs[0].set_xlabel("Time")
    axs[0].set_ylabel("Distance")
    axs[0].grid(True)

    axs[1].imshow(data[t].values, origin='lower', cmap=color)
    axs[1].imshow(frame_target, origin='lower', cmap=color_target, alpha=0.5)
    axs[1].set_title(f'Circle t = {t}')
    axs[1].axis('off')

    plt.tight_layout()
    combined_path = os.path.join(combined_output_dir, f"combined_{t:03d}.png")
    plt.savefig(combined_path)
    plt.close()

# Create combined GIF
combined_images = []
for t in range(n_times):
    filename = f"{combined_output_dir}/combined_{t:03d}.png"
    combined_images.append(imageio.imread(filename))
imageio.mimsave(combined_gif_name, combined_images, duration=0.2)
print("Combined GIF saved")
print('End of program')