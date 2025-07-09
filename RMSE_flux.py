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


#----------------------- PLOT RMSE OVER THE ABSOLUTE DIFFERENCE BETWEEN COMPARISON AND TARGET ICE FLUX AT THE GROUNDING LINE -------------------------------
# AUTHOR: marine de coatpont
# May 26, 2025
# IGE / ISMIP6 internship
#
# This script plot the RMSE over the absolute difference between comparison and target ice flux at the grounding line for the comparison done in the report.
# It plots the scatter for each models used as comparison and the linear regression for the different scenaros.
# Tho colors and the shape of the scatter are the differente scenarios.
#
# PLEASE READ README (README_SCRIPT.md) FOR MORE INFORMATION ON THIS SCRIPT
#
#------------------------------------------------------------------------------------------------------------------------------------------

df_grisli = pd.read_csv(f'{config.SAVE_PATH}/Result/Summary_LSCE_GRISLI2_2150.csv')
df_ua = pd.read_csv(f'{config.SAVE_PATH}/Result/Summary_UNN_Ua_2250.csv')
df_bed = pd.read_csv(f'{config.SAVE_PATH}/Result/Summary_BedMachine_Amundsen.csv')

flux_grisli = []
flux_ua = []
flux_bed = []

rmse_grisli = df_grisli['RMSE'].tolist()
rmse_grisli = rmse_grisli[:-1]
rmse_ua = df_ua['RMSE'].tolist()
rmse_bed = df_bed['RMSE'].tolist()
rmse_bed = rmse_bed[:-3]

for simu in config.SIMULATIONS:
    df_simu = df_grisli[df_grisli['simulation'] == simu]
    exp = df_simu['experiment'].tolist()[0]
    year_simu = df_simu['year'].tolist()[0]

    path = f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu}.nc'
    flux_comp = ismip.basin_flux_hand(xr.open_dataset(path).ligroundf, config.REGION)
    flux_grisli.append(flux_comp)

flux_grisli = np.array(flux_grisli)
path_grisli = f'{config.PATH_IF}/ligroundf_LSCE_GRISLI2_expAE04_2149.nc'
flux_target_grisli = ismip.basin_flux_hand(xr.open_dataset(path_grisli).ligroundf, config.REGION)

flux_target_grisli = float(flux_target_grisli.values)
delta_flux_grisli = np.abs(flux_grisli - flux_target_grisli)
print(delta_flux_grisli)

for simu in config.SIMULATIONS:
    df_simu = df_ua[df_ua['simulation'] == simu]
    exp = df_simu['experiment'].tolist()[0]
    year_simu = df_simu['year'].tolist()[0]

    path = f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu}.nc'
    flux_comp = ismip.basin_flux_hand(xr.open_dataset(path).ligroundf, config.REGION)
    flux_ua.append(flux_comp)

flux_ua = np.array(flux_ua)
path_ua = f'{config.PATH_IF}/ligroundf_UNN_Ua_expAE04_2250.nc'
flux_target_ua = ismip.basin_flux_hand(xr.open_dataset(path_ua).ligroundf, config.REGION)

flux_target_ua = float(flux_target_ua.values)
delta_flux_ua = np.abs(flux_ua - flux_target_ua)

for simu in config.SIMULATIONS:
    df_simu = df_bed[df_bed['simulation'] == simu]
    exp = df_simu['experiment'].tolist()[0]
    year_simu = df_simu['year'].tolist()[0]

    path = f'{config.PATH_IF}/ligroundf_{simu}_{exp}_{year_simu}.nc'
    flux_comp = ismip.basin_flux_hand(xr.open_dataset(path).ligroundf, config.REGION)
    flux_bed.append(flux_comp)

flux_bed = np.array(flux_bed)
data_bedmachine = xr.open_dataset(f'{config.SAVE_PATH}/Result/ligroundf_bedmachine.nc')
bedmachine = data_bedmachine.ligroundf
flux_target_bed = ismip.basin_flux_hand(bedmachine, config.REGION)

flux_target_bed = float(flux_target_bed.values)
delta_flux_bed = np.abs(flux_bed - flux_target_bed)

fig = plt.figure(figsize=(15, 9))

#UNN Ua
plt.scatter(delta_flux_ua, rmse_ua, color = 'deeppink', marker = 's', label = 'UNN_Ua flux')
slope_ua, intercept_ua = np.polyfit(delta_flux_ua, rmse_ua, 1)
x_vals_ua = np.linspace(min(delta_flux_ua), max(delta_flux_ua), 100)
y_vals_ua = slope_ua * x_vals_ua + intercept_ua
plt.plot(x_vals_ua, y_vals_ua, color='mediumvioletred', label=f"Linear regression: a = {slope_ua:.6f}")

#GRISLI
plt.scatter(delta_flux_grisli, rmse_grisli, color = 'mediumaquamarine', marker = 'o', label = 'LSCE_GRISLI2 flux')
slope_grisli, intercept_grisli = np.polyfit(delta_flux_grisli, rmse_grisli, 1)
x_vals_grisli = np.linspace(min(delta_flux_grisli), max(delta_flux_grisli), 100)
y_vals_grisli = slope_grisli * x_vals_grisli + intercept_grisli
plt.plot(x_vals_grisli, y_vals_grisli, color='lightseagreen', label=f"Linear regression: a = {slope_grisli:.6f}")

#BedMachine
plt.scatter(delta_flux_bed, rmse_bed, color = '#7B4DAE', marker = '^', label = 'BedMarchine flux')
slope_bed, intercept_bed = np.polyfit(delta_flux_bed, rmse_bed, 1)
x_vals_bed = np.linspace(min(delta_flux_bed), max(delta_flux_bed), 100)
y_vals_bed = slope_bed * x_vals_bed + intercept_bed
plt.plot(x_vals_bed, y_vals_bed, color='indigo', label=f"Linear regression: a = {slope_bed:.6f}")

plt.xlabel(r'$\Delta F = |F_{comparison} - F_{target}|$', fontsize = 20)
plt.ylabel('RMSE', fontsize = 20)
plt.title('RMSE over relative ice flux at the grounding line in Amundsen', fontsize = 25, weight='bold')
plt.legend()
plt.savefig(f'{config.PATH_IF}/RMSE_flux.png', dpi=300)

