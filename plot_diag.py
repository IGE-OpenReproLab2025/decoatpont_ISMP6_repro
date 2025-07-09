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

df_unn = pd.read_csv(f'{config.PATH_RMSE}/Summary_UNN_Ua_2250.csv')
df_lsce_grisli2 = pd.read_csv(f'{config.PATH_RMSE}/Summary_LSCE_GRISLI2_2150.csv')
df_BedMachine = pd.read_csv(f'{config.PATH_RMSE}/Summary_BedMachine.csv')

dfs = [df_unn, df_lsce_grisli2, df_BedMachine]

condition = ['ULB_fETISh-KoriBU2', 'UNN_Ua']

color = ListedColormap(['wheat', 'lightblue'])
color.set_bad(color='gainsboro')

for df in dfs:
    for simu in config.SIMULATIONS:
        print(f'{simu}')
        df_simu = df[df['simulation'] == simu]
        exp = df_simu['experiment'].tolist()[0]
        year_simu = df_simu['year'].tolist()[0]
        year_index = year_simu - 2016

        grounded_data = xr.open_dataset(f'{config.PATH_MASK}/{simu}/grounding_mask_{simu}_{exp}.nc')
        grounded_interp = ismip.grid_4x4(grounded_data.grounding_mask.isel(time = year_index))


        surface = ismip.open_file(simu, exp, 'orog')
        surface_interp = ismip.grid_4x4(surface.orog.isel(time = year_index))

        vx_data = ismip.open_file(simu, exp, 'xvelmean')
        vx_interp = ismip.grid_4x4(vx_data.xvelmean.isel(time = year_index))

        if simu in condition:
            vy_data = xr.open_dataset(f'{config.DATA_PATH}/{simu}/{exp}/yvelmean_AIS_{simu}_{exp}.nc', decode_times = False)
        else:
            vy_data = ismip.open_file(simu, exp, 'yvelmean')
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
        fig.text(0.01, 0.5, f'{simu} {exp} {year_simu}', va='center', rotation='vertical', fontsize=30, fontweight='bold')
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
        fig.savefig(f'{config.PATH_IF}/{simu}_{exp}_{year_simu}_diag.png', dpi = 300)
        print(f'Saved figure for {simu} {exp} {year_simu} diagnostics.')

#---------------------------------- PLOT DIAGNOSTICS FOR OBSERVATION -----------------------------------------------
# Open the observation data
target_simu = 'BedMachine'
target_data = xr.open_dataset(f'{config.SAVE_PATH}/Result/BedMachine.nc')
target_surface = target_data.surface
target_bed = target_data.bed
target_thickness = target_data.thickness

target = xr.where(target_surface - target_thickness > target_bed, 1, 0)
target_interp = ismip.grid_4x4(target)
target_mask_tot = ismip.amundsen_mask(target_interp)
target_mask = xr.where(target_mask_tot == 0, target_mask_tot, np.nan)

# Surface data
surface = ismip.grid_4x4(target_surface)
surface_mask = ismip.amundsen_mask(surface)
surface_mask = xr.where(target_mask == 0, surface_mask, np.nan)

# Velocity data
target_velo = xr.open_dataset(f'{config.SAVE_PATH}Result/antarctica_velocity_updated_v2.nc')
vx = target_velo.vx
vx = ismip.grid_4x4(vx)
vx_mask = ismip.amundsen_mask(vx)
vx_mask = xr.where(target_mask == 0, vx_mask, np.nan)

vy = target_velo.vy
vy = ismip.grid_4x4(vy)
vy_mask = ismip.amundsen_mask(vy)
vy_mask = xr.where(target_mask == 0, vy_mask, np.nan)

vitesse =  np.sqrt(vx_mask**2 + vy_mask**2)

# Plotting the diagnostics
fig, axes = plt.subplots(1, 3, figsize=(36, 10))
norm = LogNorm(vmin=vmin, vmax=vmax)
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((5,6))
# First subplot
fig.text(0.01, 0.5, 'BedMachine', va='center', rotation='vertical', fontsize=30, fontweight='bold')
pcm1 = axes[0].pcolormesh(target_mask.x, target_mask.y, target_mask, cmap=color, vmin=0, vmax=2, shading='auto')
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
#fig.savefig(f'{simu}_{exp}_{year}_diag.png', dpi = 300)
fig.savefig(f'{target_simu}_{config.REGION}_diag.png', dpi = 300)