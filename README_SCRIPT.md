# README for python scripts

This file provide explaination for the different scripts of the directory.

>[!NOTE]
> The `global` and `specific` scripts have the same processing steps therefor their description are in the same section

## compute_mask.py and compute_mask_specific.py
This script compute the grounded and floating part of the Antartic ice sheet. To do soo it uses the models output of base elevation (altitude of the lower ice surface elevation of the ice sheet) and bedrock elevation (bedrock topography):
topg - base ≈ 0 ± ε  if ice is grounded  
topg - base < 0      if ice is floating

![equation](https://latex.codecogs.com/png.image?\dpi{130}&space;\text{topg}-\text{base}=\begin{cases}0\pm\epsilon&\text{if&space;ice&space;is&space;grounded}\\<0&\text{if&space;ice&space;is&space;floating}\end{cases})

Where $\epsilon$ is a threshold value arbitrarily set to $\epsilon = 0.01$ m to compensate for numerical errors and uncertainties in the outputs of the models.

### Run the script
```bash
python3 RMSE_compute.py
```

>[!NOTE]
> Depending on your python version this command can change
### Input
For the `global script`no input needed, but for the `specific script` at runtime, the user is prompted to enter:
- `simu`: Name of the simulation to do the computation on.
- `exp`: Name of the experiment with the following format `expAEXX`.

### Proccessing steps
For each experiment of the simulation, or the chosen ones, the script compute the grounding mask at each time step. It uses the function `ismip.compute_grounded_mask` from the `ISMIP6_function.py`. This function compute the grounded part and the floating part of the ice sheet using the the definition above.

Output structure
```bash
/Result/Grounding_mask/
│── <simu>/
│   ├── grounding_mask_<expXX>.nc

```
### Example
For the specific script:
```bash
Enter the name of the simulation you want as a target (e.g ULB_fETISh-KoriBU2): UTAS_ElmerIce
Enter the experiment (e.g expAE06) or all to compute the grounded mask of all the experiment: expAE02
```

## RMSE_compute_global.py and RMSE_compute_specific.py
This script computes the Root Mean Square Error (RMSE) between a target grounding mask and those from various comparison experiments for specific years. The aim is to identify the experiment with the best agreement (i.e., lowest RMSE) with the target configuration, facilitating intercomparison of Antarctic ice sheet model behaviors.
The script also generates corresponding visual outputs and CSV files to support reproducibility and downstream analysis.

### Run the script
```bash
python3 RMSE_compute.py
```

>[!NOTE]
> Depending on your python version this command can change

### Input 
For the `global script`no input needed, but for the `specific script` at runtime, the user is prompted to enter:
- `target_simu`: Name of the target simulation (you want to compare).
- `target_exp`: Name of the target experiment with the following format `expAEXX`.
- `target_year`: One target year between 2015 and 2300

### Proccessing steps
1. Target mask extraction
For each target year, the script selects the corresponding target mask of the given simulation and experiment.

3. RMSE computation
It iterates over each simulation and its experiments, loading the associated grouding mask dataset and computing the RMSE between the target mask and each experiment mask using local function `ismip.compute_rmse()` (for more information on this function read README.md of the `Functions` directory)

4. Best match identification
For each simulation, the minimum RMSE of each experiment is identifed and save in a file `min_RMSE_<target_simu>_<target_year>_<comp_simulation>.csv`, sorted like so:
- experiment
- corresponding year
- RMSE value

In addition, a global summary `summary_min_RMSE_<target_year>` file per target year list the best match for eash simulation

5. Visualization
Plot of the RMSE over time for each simulation, all experiment are plotted on the same figure.

>[!NOTE]
>All output will be saved in your current directory

6. Output structure
```bash
/Result/RMSE/
│── <target>_<simu>/
│       ├── RMSE_<exp>_<year>.csv
│       ├── RMSE_<target>_<year>_<simu>.png
│       ├── min_RMSE_<target>_<year>_<simu>.csv
│       └── mask_<target>_<year>_<simu>.png
└── summary_min_RMSE_<year>.csv

```
### Example
For the specific script:
```bash
Enter the name of the simulation you want as a target (e.g ULB_fETISh-KoriBU2): UCM_Yelmo
Enter the experiment (e.g expAE06): expAE03
Enter the year for the target (year most be between 2015 and 2301): 2150
Enter the name of the simulation you want to compare with the target (e.g LSCE_GRISLI2): IGE_ElmerIce
```

## compute_gl_flux.py, compute_gl_flux_time.py, and specific version
This script computes the ice flux at the grounding line for the minimum simulation RMSE. It uses the following equation to compute the ice flux at the grounding line in Gt/yr:

**q(x₉) = H × v × dl**

![equation](https://latex.codecogs.com/png.image?\dpi{130}&space;q(x_g)=H\times%20v\times%20dl)

Using the models output for ice thickness and mean velocity.

Then it save the ice flux at the grounding line in netCDF file using the nomenclature: `ligroundf_{simu}_{exp}_{year}.nc` 

Differences beteween the script:
- `compute_gl_flux.py`: compute ice flux at the grounding line for the RMSE minimum from the summary file (specific year, and 5 years before and aflter the match)
- `compute_gl_flux_time.py`: compute the grounding line for all the year of the run, note that it takes a considerable amount of time.

### Run the script
```bash
python3 compute_gl_flux.py
```

>[!NOTE]
> Depending on your python version this command can change

### Input
For the `specific` script indicate:
- `target_simu`: Name of the target simulation you have done a RMSE comparison with
- `target_exp`: Name of the experiment you have done a RMSE comparison with
- `target_year`: Year with which you have done a RMSE comparison with

### Proccessing steps
1. Load RMSE summary files for the following models:
   - `UNN_Ua`
   - `LSCE_GRISLI2`
   - `BedMachine`

2. Open BedMachine dataset to use as a spatial reference for the output NetCDF grid.

3. Loop through all simulations:
   - Identify the corresponding experiment and the year with minimum RMSE.
   - Build a time window of ±5 years around the minimum RMSE year (within bounds 2017–2199).

4. For each selected year:
   - Load topography (`orog`), bedrock (`topg`), ice thickness (`lithk`), and velocity (`xvelmean`, `yvelmean`) fields.
   - Interpolate a blank NetCDF dataset to the current simulation grid.

5. Compute the grounded ice mask from: grounded_mask = |ice_base - bed| < 1e-2

6. Extract the grounding line contour using `skimage.measure.find_contours` and convert pixel coordinates into real-world coordinates.

7. Resample the contour line every 1 km for consistent resolution.

8. Interpolate fields along the resampled line:
- Ice thickness (`H`)
- Velocities (`vx`, `vy`)

9. Compute the normal component of velocity \( v_n \):
\[
v_n = vx \cdot n_x + vy \cdot n_y
\]
- Convert to m/yr
- Apply filtering for physical consistency

10. Calculate the segmental ice flux at each point:
 \[
 q(x_g) = H \times v_n \times dl
 \]
 - Units: m³/yr

11. Insert values into the output NetCDF file, mapped to the closest `(x, y)` location on the BedMachine grid.

12. Save the result as a NetCDF file:
 - Output format: `ligroundf_<simu>_<exp>_<year>.nc`


### Example
```bash
Enter the simulation name (e.g., DC_ISSM): UNN_Ua
Enter the experiment name (e.g., expAE01): expAE12
Enter the year (e.g., 2250): 2134
```

## plot_comp_flux.py and plot_comp_flux_specific.py
This script creat the comparison figure of the ice flux at the grounding line for the different target or the chosen target.
The figure is the ice flux at the grounding line over a relative time. Where t is the time of the match and the ice fluxs at the grounding line 5 year before and after are plotted.
In color the model and the shape of the scatter define the type of initialization geometry of the model.

### Run the script
```bash
python3 compute_gl_flux.py
```

>[!NOTE]
> Depending on your python version this command can change

### Input
No imput needed for the `global` script, for the `specific` script indicate:
- target_simu
- target_year

### Proccessing steps
1. Load Input Files
- Read CSV summary tables for each target model (UNN_Ua, LSCE_GRISLI2, BedMachine).
- Open `BedMachine.nc` as the reference spatial grid.

2. Compute Time Range
- Extract the year of minimum RMSE for each simulation.
- Build a time window: `year ± 5` years.

3. Load NetCDF Flux Files
- Loop through the 11 years and open corresponding NetCDF files.
- For each year:
  - Load flux values.
  - Apply a regional mask (`basin_flux_hand`) to compute total flux in the region of interest.
  - Store the flux values for plotting.

4. Build Target Curve
- For `BedMachine`, use a single year.
- For `UNN_Ua` and `LSCE_GRISLI2`, build a full 11-year time series.

5. Plotting
- For each model:
  - Plot the 11-year flux series as dashed lines with markers.
  - Use different colors, shapes, and transparencies depending on the model.
- Highlight the **target simulation** in violet (`#7B4DAE`).
- Compute and plot the **ensemble mean and standard deviation** as error bars.
- Add custom legends:
  - Marker shape: model initialization type (spin-up, mix, BedMachine)
  - Model/experiment label: simulation line
- Save final figure to: Ice_flux_<target_model>.png

### Example
```bash
Enter the simulation name (e.g., DC_ISSM): UNN_Ua
Enter the experiment name (e.g., expAE01): expAE12
Enter the year (e.g., 2250): 2134
```

## plot_diag.py and plot_diag_specific.py
This script generates a comparative visualization of grounded masks from ISMIP6 simulations relative to a target observation-based dataset (BedMachine). It overlays the model results with the target mask to assess spatial agreement in the Amundsen Embayment region.

The visual comparison highlights the mask at the year with the lowest Root Mean Square Error (RMSE) for each simulation, based on a precomputed summary table. 

### Run the scrpit
```bash
python3 plot_mask_comparison.py
```

>[!NOTE]
>Depending on your Python version, this command may vary

### Input
No user input needed, but you may want to check the path to data.

### Proccessing steps
1. Target mask computation
The target mask is derived from the BedMachine dataset unsing the difference between surface elevation and ice thickness and compared to the bedrock elevation.

2. Simulation mask loading
For each listed simulation, the script reads the year with the minimum RMSE and associated experiment frome the summary CSV. Then loads the corresponding grounding mask.

3. Visualization
Each subplot displays the simulation grounding mask overlaid with the target mask for visual comparison.

4. Output structure
A .png figure comparing the target and simulation grounding mask:
```bash
/current_diectory/
│── mask_comp_BedMachine_.png
```

## RMSE_flux.py
This script plot the RMSE (as a distance proxy) over the absolut difference of comparison and target ice flux at the grounding line. 
The goal is to acess if the difference of ice flux at the grounding line are explained by the differences in geometry.
In color are the different grounded line scenario chosen, and we add the linear regression to see if there is a corelation. 

### Run the script
```bash
python3 plot_mask_comparison.py
```

>[!NOTE]
>Depending on your Python version, this command may vary

### Input
For the `global` script there is no input needed buet for the `specific` script inform:
- target_simu: Name of the traget simulation you used
- target_exp: Name of the experiment of the simulation
- target_year: Year of the simulation for the target

### Proccessing steps
1. Read Input RMSE Tables
- Load RMSE summary CSV files for the three datasets.
- Clean the lists by removing extra rows (e.g., unused lines).

2. Compute Ice Flux for Each Simulation
- Loop over each simulation in `config.SIMULATIONS`.
- For each simulation:
  - Retrieve its associated experiment and target year from the summary table.
  - Load the corresponding `ligroundf_*.nc` file.
  - Compute the integrated grounding line flux using `ismip.basin_flux_hand()`.
  - Store the flux value.

3. Compute Target Reference Flux
- For each model family (GRISLI, Ua, BedMachine), load the **target year** NetCDF file.
- Compute the **target GL flux** in the same region.

4. Calculate ΔFlux (absolute difference)
- Compute:  
  \[
  \Delta F = |F_\text{comparison} - F_\text{target}|
  \]
- This is done separately for:
  - `flux_grisli`
  - `flux_ua`
  - `flux_bed`

5. Plotting
- For each model family:
  - Plot scatter points of (ΔFlux, RMSE).
  - Fit a linear regression:  
    \[
    \text{RMSE} = a \cdot \Delta F + b
    \]
  - Overlay the regression line and display slope `a` in the legend.

6. Export Figure
- Save final figure to:  
  `PATH_IF/RMSE_flux.png`

### Example
```bash
Enter the simulation name (e.g., DC_ISSM): UNN_Ua
Enter the experiment name (e.g., expAE01): expAE12
Enter the year (e.g., 2250): 2134
```