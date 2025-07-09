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

#----------------------- COMPUTE GROUNDED MARK FOR EVERY SIMULATION -------------------------------
#marine de coatpont
#April 18, 2025
#IGE / ISMIP6 internship
#
#
#PLEASE READ README () FOR MORE INFORMATION ON THIS SCRIPT
#
#------------------------------------------------------------------------------------------------------------------------------------------

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

for simu, nb_exp in simulation.items():
    # -------- SIMULATION AND EXPERIMENT LOOP --------
    exp_list = [f'expAE{str(i).zfill(2)}' for i in range(1, nb_exp + 1)]

    if simu == 'UNN_Ua':
        exp_list = [exp for exp in exp_list if exp not in ['expAE24']]
    if simu in vuw:
        exp_list = [exp for exp in exp_list if exp not in ['expAE08', 'expAE09']]
        
    for i, exp in enumerate(exp_list):
        grounded = ismip.compute_grounded_mask(simu, exp, config.WHERE)
        grounded.to_netcdf(f"{config.PATH_MASK}/grounding_mask_{simu}_{exp}.nc")
        print(f'Grounded mask for {simu} {exp} saved.')