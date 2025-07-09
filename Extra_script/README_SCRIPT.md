# README for python scripts
In this directory are the extra scripts used in the work but do not plot the major figure.

## RMSE_c_ircle.py
This script simulates a circle that grows over time and calculates the Root Mean Square Error (RMSE) between a fixed target circle (at time step t=50) and the growing circle at each time step.


### Run the script
```bash
python3 RMSE_circle.py
```

>[!NOTE]
> Depending on your python version this command can change

### Input
None.

### Proccessing steps
1. Define Simulation Parameters

- Grid size: `100x100`
- Time steps: `100`
- Circle growth: linearly from `r=0` to `r=max_radius` over `t=0 → t=99`

2. Create Target Circle

- Radius is set based on time step `t=50`
- A binary mask (`frame_target`) marks the inside of the circle

3. Generate Circle Growth

- For each time step:

  - Create a circle of increasing radius
  - Save image showing overlap with the target
  - Store frames in a NetCDF dataset

4. Save Outputs

- `circle_data_rmse.nc`: NetCDF file with all circle snapshots
- `circle_growth_rmse.gif`: GIF showing the growing circle
- `frame_XXX.png`: individual frame images

5. Compute RMSE

- Use `xskillscore.rmse()` to compare each time step to the target (t=50)
- Store and print RMSE values

6. Visualize RMSE Evolution

- `rmse_cercle.png`: line plot of RMSE over time
- Additional comparison plots combining:

  - RMSE up to time `t`
  - Circle snapshot at time `t`

7. Create Final Combined GIF

- Merges side-by-side comparison images into one animated GIF:

  - `combined_circle_rmse.gif`


7. Structure

``` bash
.
├── circle_data_rmse.nc              # NetCDF with all time steps
├── circle_growth_rmse.gif          # GIF of the growing circle
├── combined_circle_rmse.gif        # Final combined comparison GIF
├── rmse_cercle.png                 # RMSE over time plot
├── /circle_growth_rmse             # Raw frame images (t=0 to t=99)
├── /combined_frames_rmse           # Combined RMSE + image panels
```

### Example
none needed.