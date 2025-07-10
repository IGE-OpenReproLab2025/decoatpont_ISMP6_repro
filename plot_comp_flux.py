import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
import sys
import importlib
import pandas as pd
import os
import config


#load personal function
sys.path.append(f'{config.SAVE_PATH}/Function')
import Function.ISMIP_function as ismip
importlib.reload(ismip)


#----------------------- PLOT ICE FLUX AT THE GROUNDING LINE FOR RSME MINIMUM -------------------------------
# AUTHOR: marine de coatpont
# April 18, 2025
# IGE / ISMIP6 internship
#
#
#PLEASE READ README FOR MORE INFORMATION ON THIS SCRIPT
#
#------------------------------------------------------------------------------------------------------------------------------------------

colors = ['darkblue', 'darkturquoise', 'darkorange', 'mediumaquamarine', 'limegreen', 'tomato', 'gold', 'olive', 'deeppink', 'mediumorchid']
shapes = ['^', '^', 's', '^', 'D', 's', '^', '^', '^', '^', 'D']
alphas = [0.4, 0.4, 0.4, 0.4, 0.4, 1.0, 0.4, 0.4, 0.4, 0.4, 0.4] 
sizes = [65, 65, 65, 65, 65, 150, 65, 65, 65, 65, 65]

flux_amun = [np.full(11,np.nan)]
flux_mean = []

df_unn = f'{config.PATH_RMSE}/Summary_UNN_Ua_2250.csv'
df_lsce_grisli2 = f'{config.PATH_RMSE}/Summary_LSCE_GRISLI2_2150.csv'
df_BedMachine = f'{config.PATH_RMSE}/Summary_BedMachine.csv'

dfs = [df_unn, df_lsce_grisli2, df_BedMachine]
target_simus = ['BedMachine', 'LSCE_GRISLI2', 'UNN_Ua']

for target_simu, df_amun in zip(target_simus, dfs):
    if target_simu == 'BedMachine':
        data_bedmachine = xr.open_dataset(f'{config.SAVE_PATH}/Result/ligroundf_bedmachine.nc')
        bedmachine = data_bedmachine.ligroundf
        flux_bedmachine = ismip.basin_flux_hand(bedmachine, config.REGION, config.WHERE)
        target_year = 2015

    if target_simu == 'LSCE_GRISLI2':
        target_year = 2150   
        target_exp = 'expAE04'
        target_year = int(target_year)

        #path for the target macht and ±5
        paths_target = [
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year-5}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year-4}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year-3}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year-2}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year-1}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year+1}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year+2}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year+3}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year+4}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year+5}.nc'
               ]
        target_flux_plot = []

        for path in paths_target:
            if os.path.exists(path):
                flux_add= ismip.basin_flux_hand(xr.open_dataset(path).ligroundf, config.REGION, config.WHERE)
                target_flux_plot.append(flux_add)
            else:
                target_flux_plot.append(np.nan)

        years = [int(target_year) - 5, int(target_year) - 4, int(target_year) - 3, int(target_year) - 2, int(target_year) - 1, int(target_year), int(target_year) + 1, int(target_year) + 2, int(target_year) + 3, int(target_year) + 4, int(target_year) + 5]
    if target_simu == 'UNN_Ua':
        target_year = 2250
        target_exp = 'expAE04'
        target_year = int(target_year)

        paths_target = [
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year-5}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year-4}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year-3}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year-2}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year-1}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year+1}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year+2}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year+3}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year+4}.nc',
                f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year+5}.nc'
               ]
        target_flux_plot = []

        for path in paths_target:
            if os.path.exists(path):
                flux_add= ismip.basin_flux_hand(xr.open_dataset(path).ligroundf, config.REGION, config.WHERE)
                target_flux_plot.append(flux_add)
            else:
                target_flux_plot.append(np.nan)

        years = [int(target_year) - 5, int(target_year) - 4, int(target_year) - 3, int(target_year) - 2, int(target_year) - 1, int(target_year), int(target_year) + 1, int(target_year) + 2, int(target_year) + 3, int(target_year) + 4, int(target_year) + 5]

    
#----------------------- PLOT ICE FLUX AT THE GROUNDING LINE FOR RSME MINIMUM -------------------------------
    fig = plt.figure(figsize=(15, 9))
    ax = fig.add_axes([0.1, 0.1, 0.3, 0.6])  # [left, bottom, width, height]

    for i, simu in enumerate(config.SIMULATIONS):
        df = pd.read_csv(df_amun)
        df_simu = df[df['simulation'] == simu]
        exp = df_simu['experiment'].tolist()[0]
        year_simu = df_simu['year'].tolist()[0]

        if simu != target_simu:
            # path to comparison models
            paths = [
                f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu-5}.nc',
                f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu-4}.nc',
                f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu-3}.nc',
                f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu-2}.nc',
                f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu-1}.nc',
                f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu}.nc',
                f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu+1}.nc',
                f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu+2}.nc',
                f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu+3}.nc',
                f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu+4}.nc',
                f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu+5}.nc'
               ]

            flux = []

            for path in paths:
                if os.path.exists(path):
                    flux_add= ismip.basin_flux_hand(xr.open_dataset(path).ligroundf, config.REGION, config.WHERE)
                    flux.append(flux_add)
                else:
                    flux.append(np.nan)

            ax.plot(years, flux, linestyle='--', color=colors[i], alpha=0.5)
            ax.scatter(years, flux, label=f'{simu} {exp}, {year_simu}', color=colors[i], marker=shapes[i], alpha=alphas, s=sizes)

            flux_mean.append(flux[5])
    #mean and standard deviation
    mean = np.mean(flux_mean)
    std = np.std(flux_mean)


    # Plot target
    print(target_year)
    print(flux_bedmachine.values)
    if target_simu == 'BedMachine':
        ax.scatter(2015, 186.67325602513944, label=f'{target_simu}, {target_year}',color='#7B4DAE', s=150)
    else:
        ax.plot(years, target_flux_plot, color='#7B4DAE')
        ax.scatter(years, target_flux_plot, label=f'{target_simu}, {target_year}',color='#7B4DAE', s=sizes)
    plt.errorbar(int(target_year), mean, yerr = std, fmt = 'o', color = 'dimgray', capsize = 5)

    # Shape legend
    custom_shapes = [
    Line2D([0], [0], marker='^', color='gray', linestyle='None', label='BedMachine'),
    Line2D([0], [0], marker='s', color='gray', linestyle='None', label='Spin-up'),
    Line2D([0], [0], marker='D', color='gray', linestyle='None', label='Mix'),
    Line2D([0], [0], marker='o', color='gray', linestyle='None', label='Target')
    ]

    # Add titles to the legend
    handles, labels = ax.get_legend_handles_labels()
    simulation_legend_title = "Simulations"
    shape_legend_title = "Model initialisation"

    # Place simulation legend at the top left
    simulation_legend = ax.legend(handles, labels,
                               bbox_to_anchor=(1.05, 0.5), loc='upper left', fontsize=10, title=simulation_legend_title, frameon = False)
    simulation_legend.get_title().set_fontsize(12)
    simulation_legend.get_title().set_weight('bold')
    simulation_legend.get_title().set_horizontalalignment('left')  # Align title to the left
    ax.add_artist(simulation_legend)

    # Place shape legend at the bottom left
    shape_legend = ax.legend(custom_shapes, [s.get_label() for s in custom_shapes],
                         bbox_to_anchor=(1.05, 0.5), loc='lower left', fontsize=10, title=shape_legend_title, frameon = False)
    shape_legend.get_title().set_fontsize(12)
    shape_legend.get_title().set_weight('bold')
    shape_legend.get_title().set_horizontalalignment('left')  # Align title to the left
    ax.add_artist(shape_legend)

    ax.grid(axis='y', alpha=0.7)
    ax.set_ylim(0, 500)
    xticks = [years[0], years[5], years[-1]]  # t-5, t, t+5
    xticklabels = ['t-5', 't', 't+5']
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, fontsize=18)
    ax.tick_params(axis='y', which='major', labelsize=18)
    ax.set_title(f'Ice flux at the grounding line \n {config.REGION}', fontsize=25, weight='bold')
    ax.set_ylabel('Ice flux [Gt/yr]', fontsize=20)
    ax.set_xlabel('Years', fontsize=20)

    plt.savefig(f'{config.PATH_IF}/Ice_flux_{target_simu}.png', dpi=300)
    print(f'Saved figure for {target_simu} ice flux at the grounding line.')