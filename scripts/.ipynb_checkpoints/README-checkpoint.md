# README for python scripts

This file provide explaination for the different scripts of the directory.

## RMSE_compute.py
This script computes the Root Mean Square Error (RMSE) between a target grounding mask and those from various comparison experiments for specific years. The aim is to identify the experiment with the best agreement (i.e., lowest RMSE) with the target configuration, facilitating intercomparison of Antarctic ice sheet model behaviors.
The script also generates corresponding visual outputs and CSV files to support reproducibility and downstream analysis.

### Run the script
```bash
python3 RMSE_compute.py
```

>[!NOTE]
> Depending on your python version this command can change

### Input 
At runtime, the user is prompted to enter:
- `target_simu`: Name of the target simulation (you want to compare).
- `target_exp`: Name of the target experiment with the following format `expAEXX`.
- `target_years`: One or more target years, must be separated by comas and with no space.

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
/current_diectory/
│── <target>_<simu>/
│       ├── RMSE_<exp>_<year>.csv
│       ├── RMSE_<target>_<year>_<simu>.png
│       ├── min_RMSE_<target>_<year>_<simu>.csv
│       └── mask_<target>_<year>_<simu>.png
└── summary_min_RMSE_<year>.csv

```
### Example
```bash
Enter a simulation (e.g. ULB_fETISh-KoriBU2): PIK_PISM
Enter an experiment (e.g. expAE06): expAE07
Enter a or several target years(separated by comma): 2080,2100
```

## plot_mask_comparison.py
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