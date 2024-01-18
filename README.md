# TDE-functions
Plotting 3 point time delay estimation. 

This repository contains functions for extracting data needed to plot a 3 point time delay estimation and guides showing how to use the 3 point time delay estimation. 

There are three guides for plotting the velocity field
1. ```how_to_plot_3TDE_field_mfe.ipynb```: While working from the server, extract data and plot velocity field for Alcator C-Mod.  
2. ```how_to_plot_3TDE_field.ipynb```: Load data and plot velocity field from local machine
3. ```how_to_plot_3TDE_field_W7X.ipynb```: Load data and plot velocity field for W7X.

There are three guides 

# Dependencies
This repository depends on the following GitHub repositories:
1. To estimate 3 point velocities: https://github.com/uit-cosmo/velocity-estimation. 
2. To perform testing with synthetic data, velocity-estimation depends on https://github.com/uit-cosmo/blobmodel. 
3. To extract APD C-Mod directly from mds tree: https://github.com/sajidah-ahmed/cmod_functions
4. For detrending data - running normalization: https://github.com/uit-cosmo/fpp-analysis-tools 
5. Plotting interface: https://github.com/uit-cosmo/cosmoplots 

# Installation

```
git clone https://github.com/auroradh/TDE-functions
cd tde_functions
pip install .
```
