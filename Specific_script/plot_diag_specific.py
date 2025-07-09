import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.ticker import ScalarFormatter
from matplotlib.colors import LogNorm
import sys
import importlib
import pandas as pd
from scipy.interpolate import RegularGridInterpolator
import config

#load personal function
sys.path.append('/home/jovyan/private-storage/Decoatpont_m2_ISMP6_personal/Fonction')
import Function.ISMIP_function as ismip
importlib.reload(ismip)

#---------------------------------- PLOT DIAGNOSTICS  -----------------------------------------------
#AUTHOR: marine de coatpont
#june 12, 2025
#IGE / ISMIP6 internship
#
#
#PLEASE READ README () FOR MORE INFORMATION ON THIS SCRIPT
#
#------------------------------------------------------------------------------------------------------------------------------------------

# Choice of the simulations
target_simu = input("Enter the simulation you want to plot diagnostics for (e.g., DC_ISSM): ")
target_exp = input("Enter the experiment you want to plot diagnostics for (e.g., expAE04): ")
target_year = int(input("Enter the year you want to plot diagnostics for (e.g., '2020'): "))
year_index = target_year - 2016

condition = ['ULB_fETISh-KoriBU2', 'UNN_Ua']

color = ListedColormap(['wheat', 'lightblue'])
color.set_bad(color='gainsboro')

# Open the observation data
grounded_data = xr.open_dataset(f'{config.PATH_MASK}/{target_simu}/grounding_mask_{target_simu}_{target_exp}.nc')
grounded_interp = ismip.grid_4x4(grounded_data.grounding_mask.isel(time = year_index))

surface = ismip.open_file(target_simu, target_exp, 'orog')
surface_interp = ismip.grid_4x4(surface.orog.isel(time = year_index))

vx_data = ismip.open_file(target_simu, target_exp, 'xvelmean')
vx_interp = ismip.grid_4x4(vx_data.xvelmean.isel(time = year_index))

if target_simu in condition:
    vy_data = xr.open_dataset(f'{config.DATA_PATH}/{target_simu}/{target_exp}/yvelmean_AIS_{target_simu}_{target_exp}.nc', decode_times = False)
else:
    vy_data = ismip.open_file(target_simu, target_exp, 'yvelmean')
vy_interp = ismip.grid_4x4(vy_data.yvelmean.isel(time = year_index))

grounded_mask = ismip.amundsen_mask(grounded_interp)
vy_mask = ismip.amundsen_mask(vy_interp)
vy_mask = xr.where(grounded_mask == 0, vy_mask, np.nan)

vx_mask = ismip.amundsen_mask(vx_interp)
vx_mask = xr.where(grounded_mask == 0, vx_interp, np.nan)

surface_mask = ismip.amundsen_mask(surface_interp)
surface_mask = xr.where(grounded_mask == 0, surface_interp, np.nan)
    

#calcul de la norme
vitesse = np.sqrt(vx_mask**2 + vy_mask**2)
vitesse = vitesse * 365.25 * 24 * 3600
vmin = 1e-1
vmax = 1e3
#vmax = 1e4 #UNN_Ua
norm = LogNorm(vmin=vmin, vmax=vmax)

fig, axes = plt.subplots(1, 3, figsize=(36, 10))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((5,6))
    
# First subplot
fig.text(0.01, 0.5, f'{target_simu} {target_exp} {target_year}', va='center', rotation='vertical', fontsize=30, fontweight='bold')
pcm1 = axes[0].pcolormesh(grounded_mask.x, grounded_mask.y, grounded_mask, cmap=color, vmin=0, vmax=2, shading='auto')
handles = [
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='wheat', markersize=10, label='Grounded area'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='lightblue', markersize=10, label='Ice shelf / Open ocean'),
]
axes[0].legend(handles=handles, loc='upper right', fontsize=14)
axes[0].set_ylim(-1.0e6, 0.25e6)
axes[0].set_xlim(-2.0e6, -0.75e6)
axes[0].tick_params(axis='both', which='major', labelsize=20)
axes[0].set_aspect('equal')
axes[0].set_title("Grounded mask", fontsize=25, fontweight='bold')
axes[0].set_xlabel("x [m]", fontsize=20)
axes[0].set_ylabel("y [m]", fontsize=20)

# Second subplot
pcm2 = axes[1].pcolormesh(surface_mask.x, surface_mask.y, surface_mask, cmap='YlGnBu_r', vmin = 0, vmax = 3500, shading='auto')
axes[1].set_ylim(-1.0e6, 0.25e6)
axes[1].set_xlim(-2.0e6, -0.75e6)
axes[1].ticklabel_format(style='sci', axis='both', scilimits=(-3, 4))
axes[1].tick_params(axis='both', which='major', labelsize=20)
axes[1].set_aspect('equal')
axes[1].set_title("Surface elevation", fontsize=25, fontweight='bold')
axes[1].set_xlabel("x [m]", fontsize=20)
axes[1].set_ylabel("y [m]", fontsize=20)
cbar2 = fig.colorbar(pcm2, ax=axes[1])
cbar2.ax.set_title("Surface [m]", fontsize=18)
cbar2.ax.tick_params(labelsize=16)

# Third subplot
pcm3 = axes[2].pcolormesh(vitesse.x, vitesse.y, vitesse, cmap='Reds', norm=norm, shading='auto')
axes[2].set_ylim(-1.0e6, 0.25e6)
axes[2].set_xlim(-2.0e6, -0.75e6)
axes[2].ticklabel_format(style='sci', axis='both', scilimits=(-3, 4))
axes[2].tick_params(axis='both', which='major', labelsize=20)
axes[2].set_aspect('equal')
axes[2].set_title("Velocity norm (log scale)", fontsize=25, fontweight='bold')
axes[2].set_xlabel("x [m]", fontsize=20)
axes[2].set_ylabel("y [m]", fontsize=20)
cbar3 = fig.colorbar(pcm3, ax=axes[2], format=formatter)
cbar3.ax.set_title("Velocity [m/yr]", fontsize=18)
cbar3.ax.tick_params(labelsize=16)

plt.tight_layout()
fig.savefig(f'{config.PATH_IF}/{target_simu}_{target_exp}_{target_year}_diag.png', dpi = 300)
print(f'Saved figure for {target_simu} {target_exp} {target_year} diagnostics.')

print('Everything seems fine ~(°w°~)')
print('----- END OF PROGRAM -----')