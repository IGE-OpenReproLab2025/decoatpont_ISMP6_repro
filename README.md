# Outflow of the Antarctic ice sheet: is it consistente across models for similar geometries?

The alarming acceleration of global sea level rise rate state the importance of resolving the future climate
prediction uncertainties. The Antarctic Ice Sheet is one of the main potential contributing factor to future
sea level rise, which contribution is still the most uncertain. To account its impact we look a the ice
outflow of the AIS in a key region: the Amundsen Sea Sector.

To do so, we test Schoof 2007 [C. Schoof. Ice sheet grounding line dynamics: Steady states, stability, and hysteresis. Journal of Geophysical Research: Earth Surface, 112(F3), Sept. 2007b. doi: 10.1029/2006JF000664. URL https://doi.org/10.1029/2006JF000664.] two dimensional equation defining ice flux at the grounding line (line that separates the part of the ice sheet that is resting on the bedrock and the floating part) as a function of the sliding law, the ice rheology, and the ice thickness. Assuming that those parameters are the same across three dimensional ISMP6 model ensemble, we compare the ice flux at the grounding line.

Therefore, we find similar grounding line geometries, using RMSE, based on defined target: the observed
grounding line, a moderately retreated grounding line, and a largely retreated one (both model based).
We find that, for three dimensional models, the mean ice flux at the grounding line increase with its
retreat. Data assimilation models compute ice flux at the grounding line with a better accuracy than Spin
up models for the current grounding line geometry. However, for all the chosen targets the large ice flux
spread shows the difficulty with which models compute ice flux at the grounding line, even for models
with the same sliding law and sliding coefficient. Leading us to discuss the choice of comparison metric
and target, and looking if other regions exhibit the same results.


In this work we define three targets with which we will compare the other models with:
- `BedMachine`: target based on the observation data, this we allow us to see if the models are able to accuratly reproduce the observed geometry of the grounding line.
- `LSCE_GRISLI2 expAE04 2150`: target for the limited grounding line retreat.
- `UNN_Ua expAE04 2250`: target for the large grounding line retreat.

The model-based-target are chosen based on Seroussi 2024 [H. Seroussi, T. Pelle, W. H. Lipscomb, A. Abe-Ouchi, T. Albrecht, J.Alvarez-Solas, X. Asay-Davis, et al. Evolution of the antarctic ice sheet over the next three centuries from an ismip6 model ensemble. Earth’s Future, 12(9):e2024EF004561, Sept. 2024. doi: 10.1029/2024EF004561.], and will allow us to see if the ice flux at the grounding line increases with the retreat of the grouding. As the grounding line retreats, the ice thickness at the GL increases, which leads to an increased flux based (accordingly to Schoof 2007 equation for the ice flux at the grounding line).


## Contributors 
Marine de Coatpont

Supervisor: Gaël Durand and Cyrille Mosbeux


## Material
1. Installation of environment and data
In the directory `Installation`, you will find all the instruction needed to replicate the environment in which I worked.
The file `install_ISMP6_dataset.md` will guide you through the setup installation. 

2. Where you want your work
Modify `config.py` first two variables to stipulate where your data are stored with `DATA_PATH` and where your scripts are (where this directory is) with `SAVE_PATH`

3. Reproduce all the work of my intership
The script in this directory are all the scripts use in my internship, you can either run them individualy in the following order:

- `compute_mask.py`
- `compute_RMSE_global.py`
- `compute_gl_flux.py`
- `plot_comp_flux.py`
- `plot_diag.py`
- `RMSE_flux.py`

Or use `compute_all_work.py` script. This script will automatize running the other script in your terminal.

4. Use the scripts for your own work
You will find in `Specifi_script` the same script but for a more personal usage, you will be able to chose the target you want using input from the terminal.

>[!NOTE]
>It is still important to follow the previous order to avoid mistakes.

For more information on each script please read `README_SCRIPT.md`.

5. Result and output
All the netCDF files, figures and CSV files will be saved in the `Result` directory folowing this structure:

```bash
/all script
	|____Function/
	|	|_____ inti.py
	|		    function.py
	|
	|____ Result/
		|
		|_____ Grounded_mask/
		|	   |_____ {simu}/
		|
		|_____ RMSE/
		|	   |_____ {target_simu}_{comparison_simu}/
		|	   |	      |_____ min_{target}_{exp}.csv
		|	   |          |_____ RMSE_{target}_{year}.png
		|	   |_____ Summary_{target}_{year}.csv
		|
		|_____ Ice_flux/
        |      |_____ {simu}_{exp}_{year_simu}_diag.png
		|	   |_____ {simu}
		|		      |______ ligroundf_{simu}_{exp}_{year}.nc
		|
		|_____ Plot/

```

## Licence
Find in `license.txt` for more information