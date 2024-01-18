# TDE-functions
Plotting 3 point time delay estimation. 

This repository contains functions for extracting data needed to plot a 3 point time delay estimation. It also contains a guide showing how to use the 3 point time delay estimation method and how to plot the resulting velocity field for Alcator C-Mod and W7X.

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
