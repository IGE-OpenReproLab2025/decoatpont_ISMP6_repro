import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import sys
import importlib
import pandas as pd
import os
import config

#load personal function
sys.path.append(f'{config.SAVE_PATH}/Fonction')
import Function.ISMIP_function as ismip
importlib.reload(ismip)

#---------------------------- COMPUTE GROUNDED MARK FOR EVERY SIMULATION -----------------------------------------------------------
#
# AUTHOR: Marine de Coatpont
# May 5, 2025
# IGE / ISMIP6 internship
#
# This script computes the grounded mask for a specific simulation and experiment. 
# It uses the same function as the one used in the compute_mask.py script (function in ISMIP6_function.py).
#
#PLEASE READ README (README_SCRIPT.md) FOR MORE INFORMATION ON THIS SCRIPT
#
#------------------------------------------------------------------------------------------------------------------------------------------


# Choice of the simulation and experiment
simu = input('Enter the name of the simulation you want as a target (e.g ULB_fETISh-KoriBU2): ')
exp = input('Enter the experiment (e.g expAE06) or all to compute the grounded mask of all the experiment: ')

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
}

vuw = ['VUW_PRISM1', 'VUW_PRISM2']

if exp.lower() == 'all':
    exp_list = [f'expAE{str(i).zfill(2)}' for i in range(1, simulation[simu] + 1)]
else:
    exp_list = [exp]

if simu == 'UNN_Ua':
    exp_list = [exp for exp in exp_list if exp not in ['expAE24']]
if simu in vuw:
    exp_list = [exp for exp in exp_list if exp not in ['expAE08', 'expAE09']]
     
for exp in enumerate(exp_list):
    grounded = ismip.compute_grounding_mask_time(simu, exp)
    save_dir = f'{config.PATH_MASK}/{simu}'
    os.makedirs(save_dir, exist_ok=True)
    grounded.to_netcdf(f"{save_dir}/grounding_mask_{simu}_{exp}.nc")
    print(f'Grounded mask for {simu} {exp} saved.')