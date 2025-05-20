import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import xskillscore as xs
import sys
import importlib
import pandas as pd
import os

#load personal function
sys.path.append('/home/jovyan/private-storage/Decoatpont_m2_ISMP6_personal/Fonction')
import ISMIP_function as ismip
importlib.reload(ismip)

#---------------------------------- PLOT MIN RMSE OF TARGET AND COMPARAISON GROUNDED MASK  -----------------------------------------------
#marine de coatpont
#April 18, 2025
#IGE / ISMIP6 internship
#
#
#PLEASE READ README () FOR MORE INFORMATION ON THIS SCRIPT
#
#------------------------------------------------------------------------------------------------------------------------------------------
print('----- BEGINING OF PLOT COMPARISON MASK PROGRAM -----')
print('Begining of comutation for target mask')

#parameters
where = 'j'

#target simulation
target_simu = 'BedMachine'
target_data = xr.open_dataset('/home/jovyan/private-storage/result/BedMachineAntarctica.nc')
target_surface = target_data.surface
target_bed = target_data.bed
target_thickness = target_data.thickness

#computation on the obs to get 
target = xr.where(target_surface - target_thickness > target_bed, 1, 0)
target_interp = ismip.grid_4x4(target)
target_mask = ismip.amundsen_mask(target_interp, where)
print('End of computation for target mask')

#comparaison simulation
#definition of the simulations and assosiated experiment
simulation = ['DC_ISSM','IGE_ElmerIce','ILTS_SICOPOLIS','LSCE_GRISLI2','NORCE_CISM2-MAR364-ERA-t1','PIK_PISM','UCM_Yelmo','ULB_fETISh-KoriBU2','UNN_Ua','UTAS_ElmerIce','VUW_PRISM1','VUW_PRISM2']

#set the colors for the plot
color = ListedColormap(['wheat', 'aliceblue'])
color.set_bad(color='lightgrey')
color_target = ListedColormap(['indianred'])

#creation of the figure
fig, axes = plt.subplots(5, 3, figsize=(18, 18))
axes = axes.flatten()

print('Begining of computation for simulations')
for i, simu in enumerate(simulation):
    #table of RMSE minimum for each comparaison experiment 
    df = pd.read_csv('/home/jovyan/private-storage/Decoatpont_m2_ISMP6_personal/2025-05-06/Summary_BedMachine.csv')
    df_simu = df[df['simulation'] == simu]
    exp = df_simu['experiment'].tolist()[0]
    year_simu = df_simu['year'].tolist()[0]
    year_index = year_simu - 2016
    rmse = df_simu['RMSE'].tolist()[0]

    data = xr.open_dataset(f'/home/jovyan/private-storage/result/Grounding_mask/{simu}/grounding_mask_{simu}_{exp}.nc', decode_times=False)
    data_mask_total = data.grounding_mask.isel(time=year_index)
    data_interp = ismip.grid_4x4(data_mask_total)
    data_mask = ismip.amundsen_mask(data_interp, where)
    
    if i >= len(axes):
        break

    ax = axes[i]

    pcm1 = ax.pcolormesh(data_mask.x, data_mask.y, data_mask, cmap=color, vmin=0, vmax=2, shading='auto')#comparaison mask
    pcm2 = ax.pcolormesh(target_mask.x, target_mask.y, target_mask, cmap=color_target, alpha=0.45, shading='auto')#target mask

    #caption
    if i == 0:
        handles = [
            plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='wheat', markersize=10, label='Grounded (0)'),
            plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='aliceblue', markersize=10, label='Ocean (2)'),
            plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='indianred', markersize=10, alpha=0.4, label='Target grounded (fETISh)')
            ]
        ax.legend(handles=handles, loc='upper right', fontsize=9)
    ax.set_ylim(-1.0e6, 0.25e6)
    ax.set_xlim(-2.0e6, -0.75e6)
    ax.set_aspect('equal')
    ax.set_title(f"{simu} {exp} : {year_simu}, rmse = {rmse:.4f}", fontsize=12)
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    print(f'{simu} plotted')

#remove none existing figures
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

print('End of computation for simulations')
fig.tight_layout()
fig.subplots_adjust(top=0.92)
fig.suptitle(f"Comparison of grounding masks from {target_simu} and all simulation at RMSE minimum years", fontsize=20)
fig.savefig(f"/home/jovyan/private-storage/result/RMSE/mask_comp_{target_simu}_.png", dpi=300)

print('Everything seems fine ~(°w°~)')
print('All done - end of program')