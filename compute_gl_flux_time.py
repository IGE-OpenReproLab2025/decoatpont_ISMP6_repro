import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import sys
import importlib
import pandas as pd
from scipy.interpolate import RegularGridInterpolator
from skimage import measure
import config

#load personal function
sys.path.append(f'{config.SAVE_PATH}/Fonction')
import Function.ISMIP_function as ismip
importlib.reload(ismip)

#---------------------------------- COMPUTATION OF ICE FLUX AT THE GROUNDING LINE  -----------------------------------------------
#AUTHOR: CYRILLE MOSBEUX
#MODIFICATION: marine de coatpont
#April 18, 2025
#IGE / ISMIP6 internship
#
#
#PLEASE READ README () FOR MORE INFORMATION ON THIS SCRIPT
#
#------------------------------------------------------------------------------------------------------------------------------------------

# === Resample Grounding Line ===
def resample_line(x, y, spacing):
    dists = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
    dist_cum = np.concatenate([[0], np.cumsum(dists)])
    n_points = int(dist_cum[-1] // spacing)
    new_distances = np.linspace(0, dist_cum[-1], n_points)
    x_new = np.interp(new_distances, dist_cum, x)
    y_new = np.interp(new_distances, dist_cum, y)
    return x_new, y_new


# === Interpolate Fields at GL Points ===
def interp_field(field):
    interp = RegularGridInterpolator((y, x), field.values, bounds_error=False, fill_value=np.nan)
    return interp(np.column_stack((y_gl, x_gl)))


print('----- BEGINING OF PLOT PROGRAM -----')

# === Parameters ===
grounding_line_level = 0.0  # Bed at sea level
density_ice = 917  # kg/m³
resample_spacing = 1000  # meters
max_velocity_threshold = 2000  # m/yr
where = 'j'

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

vuw = ['VUW_PRISM1', 'VUW_PRISM2']



for simu, nb_exp in simulation.items():
    # -------- SIMULATION AND EXPERIMENT LOOP --------
    print(f'Computation for {simu}:')
    exp_list = [f'expAE{str(i).zfill(2)}' for i in range(1, nb_exp + 1)]

    if simu == 'UNN_Ua':
        exp_list = [exp for exp in exp_list if exp not in ['expAE24']]
    if simu in vuw:
        exp_list = [exp for exp in exp_list if exp not in ['expAE08', 'expAE09']]
        
    for i, exp in enumerate(exp_list):
        #file for hand computation
        ds_orog = ismip.open_file(simu, exp, 'orog', where)
        ds_topg = ismip.open_file(simu, exp, 'topg', where)
        ds_thk = ismip.open_file(simu, exp, 'lithk', where)
        
        ds_vx = ismip.open_file(simu, exp, 'xvelmean', where)
        ds_vy = ismip.open_file(simu, exp, 'yvelmean', where)

        # === Initialize Output Dataset ===
        flux_ds = xr.zeros_like(ds_orog).rename({'orog': 'ligroundf'})
        flux_ds['ligroundf'].attrs.update({
            'units': 'Gt yr⁻¹',
            'long_name': 'Ice flux at the grounding line',
            'standard_name': 'grounding_line_flux'
        })
        flux_ds.attrs.update({
            'title': 'Grounding line ice flux time series',
            'summary': 'Mass fluxes computed along the Antarctic grounding line for each year',
            'source': 'ISMIP6 model outputs',
            'history': 'Created on 2025-05-14 using custom script',
            'comment': 'Computed using custom script and ISMIP6 outputs',
            'Conventions': 'CF-1.8',
            'note': 'Resampled to 1 km resolution along grounding line'
        })

        for time in range (len(ds_orog.time)):
            print(f'{exp}: Year {time + 1}/{len(ds_orog.time)}')
            
            # === Homemade computation ===
            surface = ds_orog["orog"].isel(time=time)
            bed = ds_topg["topg"].isel(time=time)
            thickness = ds_thk["lithk"].isel(time=time)
            vx = ds_vx["xvelmean"].isel(time=time)
            vy = ds_vy["yvelmean"].isel(time=time)
            ice_base = (surface - thickness)

            grounded_mask = np.abs(ice_base - bed).values < 1e-2  # Boolean grounded mask
            gl_mask = grounded_mask.astype(float)

            x = bed["x"].values
            y = bed["y"].values

            # Find contours at the 0.5 level = boundary between grounded (1) and ungrounded (0)

            contours = measure.find_contours(grounded_mask, level=0.5)

            if not contours:
                raise RuntimeError("No contour found at level 0.5 — check your data.")


            contour = max(contours, key=len)
            contour_y, contour_x = contour.T  # in pixel coords


            dx = x[1] - x[0]
            dy = y[1] - y[0]
            x_real = x[0] + contour_x * dx
            y_real = y[0] + contour_y * dy

            x_gl, y_gl = resample_line(x_real, y_real, resample_spacing)
            vx_gl = interp_field(vx)
            vy_gl = interp_field(vy)
            H_gl = interp_field(thickness)

            # Compute normals
            dx = np.gradient(x_gl)
            dy = np.gradient(y_gl)
            dl = np.sqrt(dx**2 + dy**2)
            nx = dy / dl
            ny = -dx / dl

            vn = vx_gl * nx + vy_gl * ny
            vn =vn * 365.25 * 24 * 3600  # Convert to m/yr
            vn[np.isnan(vn)] = 0
            vn[vn > max_velocity_threshold] = 0.1

            # Compute Segmental Flux
            flux = H_gl * vn * dl#m3/yr
            flux[np.isnan(flux)] = 0
            total_flux_kg_per_yr = np.sum(flux) * density_ice
            total_flux_Gt_per_yr = total_flux_kg_per_yr / 1e12
            mass_flux = flux / dl / 1e6 # Gt/yr

            #loop on coordinates in order to have a dataset
            print('converting to dataset')

            for i, (x_line, y_line) in enumerate(zip(x_gl, y_gl)):
                selected_point = flux_ds.ligroundf.isel(time = time).sel(x=x_line, y=y_line, method='nearest')

                x_idx, y_idx = selected_point.x.values, selected_point.y.values

                flux_ds.ligroundf.isel(time = time).loc[dict(x=x_idx, y=y_idx)] += flux[i]

        # === Save NetCDF ===
        nc_path = f'/home/jovyan/private-storage/result/Flux/ligroundf_{simu}_{exp}.nc'
        flux_ds.to_netcdf(nc_path)
        print('netCDF saved!')



