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
sys.path.append('/home/jovyan/private-storage/Decoatpont_m2_ISMP6_personal/Fonction')
import Function.ISMIP_function as ismip
importlib.reload(ismip)


#----------------------- PLOT RMSE OVER THE ABSOLUTE DIFFERENCE BETWEEN COMPARISON AND TARGET ICE FLUX AT THE GROUNDING LINE -------------------------------
# AUTHOR: marine de coatpont
# May 26, 2025
# IGE / ISMIP6 internship
#
#
# PLEASE READ README FOR MORE INFORMATION ON THIS SCRIPT
#
#------------------------------------------------------------------------------------------------------------------------------------------

# Choice of the simulations
target_simu = input("Enter the simulation you want to plot ice flux for (e.g., DC_ISSM): ")
target_exp = input("Enter the experiment you want to plot ice flux for (e.g., expAE04): ")
target_year = int(input("Enter the year you want to plot ice flux for (e.g., '2020'): "))

df = pd.read_csv(f'{config.SAVE_PATH}/Result/Summary_{target_simu}_{target_year}.csv')

flux = []
rmse = df['RMSE'].tolist()

for simu in config.SIMULATIONS:
    df_simu = df[df['simulation'] == simu]
    exp = df_simu['experiment'].tolist()[0]
    year_simu = df_simu['year'].tolist()[0]

    path = f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu}.nc'
    flux_comp = ismip.basin_flux_hand(xr.open_dataset(path).ligroundf, config.REGION)
    flux.append(flux_comp)

flux_grisli = np.array(flux)
path = f'{config.PATH_IF}/ligroundf_{target_simu}_{target_exp}_{target_year}.nc'
flux_target = ismip.basin_flux_hand(xr.open_dataset(path).ligroundf, config.REGION)

flux_target = float(flux_target.values)
delta_flux = np.abs(flux_grisli - flux_target)


fig = plt.figure(figsize=(15, 9))
plt.scatter(delta_flux, rmse, color = 'mediumaquamarine', marker = 'o', label = 'LSCE_GRISLI2 flux')
slope_grisli, intercept_grisli = np.polyfit(delta_flux, rmse, 1)
x_vals_grisli = np.linspace(min(delta_flux), max(delta_flux), 100)
y_vals_grisli = slope_grisli * x_vals_grisli + intercept_grisli
plt.plot(x_vals_grisli, y_vals_grisli, color='lightseagreen', label=f"Linear regression: a = {slope_grisli:.6f}")

plt.xlabel(r'$\Delta F = |F_{comparison} - F_{target}|$', fontsize = 20)
plt.ylabel('RMSE', fontsize = 20)
plt.title('RMSE over relative ice flux at the grounding line in Amundsen', fontsize = 25, weight='bold')
plt.legend()
plt.savefig(f'{config.PATH_IF}/RMSE_flux_{target_simu}_{target_year}.png', dpi=300)

