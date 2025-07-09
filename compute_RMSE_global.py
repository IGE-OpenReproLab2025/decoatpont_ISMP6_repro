import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import xskillscore as xs
import sys
import importlib
import pandas as pd
import os
import config

#load personal function
sys.path.append('/home/jovyan/private-storage/Decoatpont_m2_ISMP6_personal/Fonction')
import Function.ISMIP_function as ismip
importlib.reload(ismip)

#---------------------------------- COMPUTATION OF ITHE RMSE BETWEEN REPORT TARGET AND ALL THE OTHER SIMULATION  -----------------------------------------------
#
# Author: marine de coatpont
# April 18, 2025
# IGE / ISMIP6 internship
#
# This script compute the RMSE for the target models chosen in the intersiph report.
# The computation of the RMSE is done using xskillscore (a python library for netCDF computation)
#
# The RMSE between each simulation and the target are save in a CSV file in the corresponding directory following this name tag: {target_simu}_{simu}/RMSE_{exp}.csv
# Other file are saved, figure of the RMSE over the time and the summary of the minimum of RMSE for each simulation
#
#------------------------------------------------------------------------------------------------------------------------------------------
#
# PLEASE READ README (README_SCRIPT.md) FOR MORE INFORMATION ON THIS SCRIPT
#
#------------------------------------------------------------------------------------------------------------------------------------------

targets = ['LSCE_GRISLI2', 'UNN_Ua', 'BedMachine']

#definition of the simulations and assosiated experiment
simulation = {
    'DC_ISSM' : 10 ,
    'IGE_ElmerIce' : 6,
    'ILTS_SICOPOLIS' : 14,
    'LSCE_GRISLI2' : 14,
    'NORCE_CISM2-MAR364-ERA-t1' : 6,
    'PIK_PISM' : 10,
    'UCM_Yelmo' : 14,
    'ULB_fETISh-KoriBU2' : 14,
    'UNN_Ua' : 30,
    'UTAS_ElmerIce' : 10,
    'VUB_AISMPALEO' : 10,
    'VUW_PRISM1' : 10,
    'VUW_PRISM2' : 10,
}

vuw = ['VUW_PRISM1', 'VUW_PRISM2'] #for a following condition

# Other parameters
min_table = []
summary_table = []
colors = plt.get_cmap('tab20').colors

for target_simu in targets:
    if target_simu == 'BedMachine':
        target_data = xr.open_dataset(f'{config.SAVE_PATH}/Result/BedMachine.nc')
        target_surface = target_data.surface
        target_bed = target_data.bed
        target_thickness = target_data.thickness

        #computation on the obs to get 
        target_mask = xr.where(target_surface - target_thickness > target_bed, 1, 0)
    
    if target_simu == 'LSCE_GRISLI2':
        target_exp = 'expAE04'
        target_year = 2150
        target_index = target_year - 2016
        target_data = xr.open_dataset(f'{config.PATH_MASK}/{target_simu}/grounding_mask_{target_simu}_{target_exp}.nc')
        target_mask = target_data.grounding_mask.isel(time = target_index)
    
    if target_simu == 'UNN_Ua':
        target_exp = 'expAE04'
        target_year = 2250
        target_index = target_year - 2016
        target_data = xr.open_dataset(f'{config.PATH_MASK}/{target_simu}/grounding_mask_{target_simu}_{target_exp}.nc')
        target_mask = target_data.grounding_mask.isel(time = target_index)

    for simu, nb_exp in simulation.items():
        # -------- SIMULATION AND EXPERIMENT LOOP --------
        print(f'Computation for {simu}')
        min_table_simu = []

        exp_list = [f'expAE{str(i).zfill(2)}' for i in range(1, nb_exp + 1)]

        #some simulation don't have all the experiment
        if simu == 'UNN_Ua':
            exp_list = [exp for exp in exp_list if exp not in ['expAE24']]
        if simu in vuw:
            exp_list = [exp for exp in exp_list if exp not in ['expAE08', 'expAE09']]
        
        plt.figure(figsize=(12, 6))
        for i, exp in enumerate(exp_list):
            print(f'{exp} ({i}/{len(exp_list)})')
            comp_data = xr.open_dataset(f'{config.PATH_MASK}/{simu}/grounding_mask_{simu}_{exp}.nc')

            #RMSE computation using local function
            rmse_target_comp = ismip.compute_rmse(target_mask, comp_data, config.REGION)

            time = comp_data.time.values
            years = comp_data.time.dt.year.values

            min_rmse = np.nanmin(rmse_target_comp)
            min_year = years[np.nanargmin(rmse_target_comp)]

            #add to min_table
            min_table_simu.append({'experiment': exp, 'min_RMSE': min_rmse, 'min_year': min_year})

            #plot RMSE during time
            color = colors[i % len(colors)]

            plt.plot(years, rmse_target_comp, color=color, label=f'{simu} {exp} (min={min_rmse:.4f} in {min_year})')

            #save RSME in csv
            df = pd.DataFrame({"time": time, "year": years, "rmse" : rmse_target_comp})

            save_dir = f'{config.PATH_RMSE}/{target_simu}_{simu}'
            os.makedirs(save_dir, exist_ok=True)

            df.to_csv(f'{save_dir}/RMSE_{exp}.csv', index=False)
            print(f'CSV file {exp} saved successfully!')

        min_df = pd.DataFrame(min_table_simu)
        min_df.to_csv(f'{save_dir}/min_RMSE_{target_simu}_{simu}.csv', index=False)
        print(f"Minimum table {target_simu} {simu} saved successfully")
        
        #plot
        plt.title(f'RMSE of {target_simu} {target_exp} and {simu} experiments', fontsize=18)
        plt.xlabel('Year')
        plt.ylabel('RMSE')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'{save_dir}/RMSE_{target_simu}_{target_year}_{simu}.png', dpi=300)
        print('Figure saved successfully')
        
        #global summary CSV 
        mini = pd.read_csv(f'{save_dir}/min_RMSE_{target_simu}_{simu}.csv')
        rmse = mini['min_RMSE'].values
        date = mini['min_year'].values
        experiment = mini['experiment'].values
        mini_rmse = np.nanmin(rmse)
        mini_exp = experiment[np.nanargmin(rmse)]
        mini_year = date[np.nanargmin(rmse)]

        summary_table.append({'simulation': simu, 'experiment': mini_exp, 'year': mini_year, 'RMSE': mini_rmse})
        print(f'All done for {simu}')

    summary_df = pd.DataFrame(summary_table)
    summary_df.to_csv(f'{config.PATH_RMSE}/Summary_{target_simu}_{simu}.csv', index=False)
    print(f'CSV summary file {target_simu} {simu} saved successfully')