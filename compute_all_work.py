import os
import config
# Creation of the structure

# Compute the grounded mask
print('Begining of the computation of the grounded mask')
os.system(f"python3 {config.SAVE_PATH}/compute_mask.py")
print('Grounded mask computed and saved in the Result folder')

# Compute RMSE comparison
print('Begining of the computation of the RMSE')
os.system(f"python3 {config.SAVE_PATH}/compute_RMSE_global.py")
print('RMSE comparison computed and saved in the Result folder')

# Compute the ice flux at the grounding line
print('Begining of the computation of the ice flux at the grounding line')
os.system(f"python3 {config.SAVE_PATH}/compute_gl_flux.py")
print('Ice flux at the grounding line computed and saved in the Result folder')

# Plot of the ice flux comparison
print('Begining of the creation of the ice flux comparison figure')
os.system(f"python3 {config.SAVE_PATH}/plot_comp_flux.py")
print('Ice flux comparison figure saved in the Result folder')

# Plot of the diagnostics
print('Begining of the creation of the diagnostics figure')
os.system(f"python3 {config.SAVE_PATH}/plot_diag.py")
print('Diagnostics figure saved in the Result folder')

# Plot of the RMSE comparison
print('Begining of the creation of the RMSE comparison figure')
os.system(f"python3 {config.SAVE_PATH}/RMSE_flux.py")
print('RMSE comparison figure saved in the Result folder')

print('Everything seems fine ~(°w°~)')
print('----- END OF PROGRAM -----')