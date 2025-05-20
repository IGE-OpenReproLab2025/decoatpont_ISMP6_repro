import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import sys
import importlib
import pandas as pd
from scipy.interpolate import RegularGridInterpolator
from skimage import measure

#load personal function
sys.path.append('/home/jovyan/private-storage/Decoatpont_m2_ISMP6_personal/Fonction')
import ISMIP_function as ismip
importlib.reload(ismip)

#---------------------------------- COMPUTATION OF ICE FLUX AT THE GROUNDING LINE  -----------------------------------------------
#AUTHOR: marine de coatpont
#April 18, 2025
#IGE / ISMIP6 internship
#
#
#PLEASE READ README () FOR MORE INFORMATION ON THIS SCRIPT
#
#------------------------------------------------------------------------------------------------------------------------------------------

print('----- BEGINING OF PLOT PROGRAM -----')

# === Parameters ===
density_ice = 917  # kg/m³
teal = '0E8278'
orange = 'F29238'
where = 'j'
region = 'Amundsen'
simulations = ['UNN_Ua']#['ULB_fETISh-KoriBU2', 'LSCE_GRISLI2', 'PIK_PISM', 'UCM_Yelmo', 'ULB_fETISh-KoriBU2', 
year = np.linspace(2016, 2031, 286)

# === Load Summary CSV ===
df = pd.read_csv('/home/jovyan/private-storage/Decoatpont_m2_ISMP6_personal/2025-05-12/Summary_BedMachine_Amundsen.csv')

for simu in simulations:
    print(f'Computation for {simu}')
    df_simu = df[df['simulation'] == simu]
    exp = df_simu['experiment'].tolist()[0]
    year_simu = df_simu['year'].tolist()[0]

    # === Load Data ===
    #computation with output file
    data = ismip.open_file(simu, exp, 'ligroundf', where)

    #homemade computation
    data_hand = xr.open_dataset(f'/home/jovyan/private-storage/result/ligroundf_{simu}_{exp}.nc')
    flux_year, flux_year_hand = [], []

    fig, ax = plt.subplots(figsize = (12, 6))

    for time in range (len(data.time)):
        print(f'Year {time + 1}/{len(data.time)}')
        
        # === Flux from ISMIP output ===
        flux = ismip.basin_flux(data.ligroundf.isel(time = time), simu, region, where)
        flux_year.append(flux)

        flux_hand = ismip.basin_flux_hand(data_hand.ligroundf.isel(time = time), region, where)
        flux_year_hand.append(flux_hand)

    # === Plotting ===
    ax.plot(data.time.dt.year.values, flux_year, color = '#0E8278', label = f'{simu} output')
    ax.plot(data.time.dt.year.values, flux_year_hand, color = '#F29238', label = 'Recalculated flux')
    ax.axvline(year_simu, linestyle = '--', color='black', alpha = 0.2, label = 'Year of comparison with target')
    ax.set_xlabel('Time in year')
    ax.set_ylabel('Ice flux [Gt/yr]')
    ax.legend()
    ax.set_title(f'Ice flux at the grounding line in {region} region for {simu} {exp}')
    
    fig.savefig(f'/home/jovyan/private-storage/result/ice_flux_{simu}_{region}.png', dpi = 300)

print('Everything seems fine ~(°w°~)')
print('All done - end of program')