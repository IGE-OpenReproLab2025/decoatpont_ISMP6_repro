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


#----------------------- COMPUTE RMSE FOR A TARGET MASK AT A GIVEN YEAR AND EXPERIMENT OF ANOTHER SIMULATION -------------------------------
#marine de coatpont
#April 18, 2025
#IGE / ISMIP6 internship
#
#
#PLEASE READ README FOR MORE INFORMATION ON THIS SCRIPT
#
#------------------------------------------------------------------------------------------------------------------------------------------
print('----- BEGINING OF RMSE COMPUTATION PROGRAM -----')

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

vuw = ['VUW_PRISM1', 'VUW_PRISM2']#for a following condition

#target mask parameters
print('--- Selection of the target mask ---')
target_simu = input('Enter a simulation (e.g ULB_fETISh-KoriBU2): ')
target_exp = input('Enter an experiment (e.g expAE06): ')
target_year_str = input('Enter a or several target years(separated by coma): ')

target_year = [int(a.strip()) for a in target_year_str.split(',') if a.strip()]
target_index = [a - 2016 for a in target_year]

target_data = xr.open_dataset(f'/home/jovyan/private-storage/result/Grounding_mask/{target_simu}/grounding_mask_{target_simu}_{target_exp}.nc')

#other parameters
where = 'j'

#colors
colors = plt.get_cmap('tab20').colors
color_comp = ListedColormap(['wheat', 'aliceblue'])
color_comp.set_bad(color='lightgrey')
color_target = ListedColormap(['indianred'])


print('--- Begining of computation ---')

for index in target_index:
    # -------- TIME LOOP --------
    #selection of the target mask
    target_mask = target_data.grounding_mask.isel(time = index)
    target_mask_plot = xr.where(target_mask == 0, 1, np.nan)
    
    year_index = index + 2016
    summary_table = []
    print(f'COMPUTATION FOR {year_index}:')
    for simu, nb_exp in simulation.items():
        # -------- SIMULATION AND EXPERIMENT LOOP --------
        print(f'Computation for {simu}:')
        min_table_simu = []
        plt.figure(figsize=(12, 6))
        exp_list = [f'expAE{str(i).zfill(2)}' for i in range(1, nb_exp + 1)]

        #some simulation don't have all the experiment
        if simu == 'UNN_Ua':
            exp_list = [exp for exp in exp_list if exp not in ['expAE24']]
        if simu in vuw:
            exp_list = [exp for exp in exp_list if exp not in ['expAE08', 'expAE09']]
        
        for i, exp in enumerate(exp_list):
            print(f'{exp} ({i}/{len(exp_list)})')
            comp_data = xr.open_dataset(f'/home/jovyan/private-storage/result/Grounding_mask/{simu}/grounding_mask_{simu}_{exp}.nc')

            #RMSE computation using local function
            rmse_target_comp = ismip.compute_rmse(target_mask, comp_data, where)
            print('RMSE computation finished')

            time = comp_data.time.values
            years = comp_data.time.dt.year.values

            min_rmse = np.nanmin(rmse_target_comp)
            min_year = years[np.nanargmin(rmse_target_comp)]
            print(f'Minimale RMSE for {exp} is: {min_rmse:.4f} in {min_year}')

            #add to min_table
            min_table_simu.append({'experiment': exp, 'min_RMSE': min_rmse, 'min_year': min_year})

            #save RSME in csv
            df = pd.DataFrame({"time": time, "year": years, "rmse" : rmse_target_comp})
            save_dir = f'{target_simu}_{simu}'
            os.makedirs(save_dir, exist_ok=True)
            df.to_csv(f'{save_dir}/RMSE_{exp}_{year_index}.csv', index=False)
            print(f'CSV file {exp} saved successfully!')

            #Plot experiment RMSE vs years
            color = colors[i % len(colors)]
            plt.plot(years, rmse_target_comp, color=color, label=f'{simu} {exp} (min={min_rmse:.4f} in {min_year})')
        
        plt.title(f'RMSE between {target_simu} {target_exp} and other experiments for {year_index}', fontsize=18)
        plt.xlabel('Year')
        plt.ylabel('RMSE')
        plt.legend(fontsize=8)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'{save_dir}/RMSE_{target_simu}_{year_index}.png', dpi=300)
        plt.close()
        print(f'Figure {target_simu} {year_index} saved successfully')
        
        #CSV file for each simulation
        min_df = pd.DataFrame(min_table_simu)
        min_df.to_csv(f'{save_dir}/min_RMSE_{target_simu}_{year_index}_{simu}.csv', index=False)
        print(f"Minimum table {target_simu} {year_index} {simu} saved successfully")
        
        #global summary CSV 
        mini = pd.read_csv(f'{save_dir}/min_RMSE_{target_simu}_{year_index}_{simu}.csv')
        rmse = mini['min_RMSE'].values
        date = mini['min_year'].values
        experiment = mini['experiment'].values
        mini_rmse = np.nanmin(rmse)
        mini_exp = experiment[np.nanargmin(rmse)]
        mini_year = date[np.nanargmin(rmse)]

        summary_table.append({'simulation': simu, 'experiment': mini_exp, 'year': mini_year, 'RMSE': mini_rmse})
        print(f'All done for {simu}')

    summary_df = pd.DataFrame(summary_table)
    summary_df.to_csv(f'Summary_{target_simu}_{simu}_{year_index}.csv', index=False)
    print(f'CSV summary file {target_simu} {simu} saved successfully')
    print(f'All done for {year_index}')

print('Everything seems fine ~(°w°~)')
print('----- END OF PROGRAM -----')