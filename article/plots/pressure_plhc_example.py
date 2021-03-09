# MIT License
# 
# Copyright (c) 2021 Pierre-Yves Camille Regis Taunay
#  
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
File: pressure_plhc_example.py
Author: Pierre-Yves Taunay
Date: March, 2021
Description: generate Fig. 13e in Part 1 of Physics of Thermionic Orificed Hollow Cathodes.
The data presented are for a neutral gas temperature of 3000 K
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### Path to HDF5 file
path_to_results = '../../results/plhc.h5'

### Generate a dataframe out of results for the following parameters:
# Discharge current = 100-307 A
# Mass flow rate = 109 sccm
# Neutral gas temperature = 3000 K
# Sheath voltage = 1-10 V
key_root = 'Ar/simulations/results/'
key_end = ['r20210309173700']
TgK = 3000

# Create a list for each dataframe
dlist = []
for ke in key_end:
    # Create the key
    # 'Xe/simulations/results/<temperature>/insert/r<UTC time results were written>'
    key = key_root + str(TgK) + '/insert/' + ke
    
    # Read the dataframe
    d = pd.read_hdf(path_to_results,key=key)
    dlist.append(d)

# Append everything to the first dataframe
for d in dlist[1:]:
    dlist[0] = dlist[0].append(d)

# Aggregate dataframe
dfall = dlist[0].copy()

fig, ax = plt.subplots(1,1)

### Get data for mass flow of 109 sccm
dfx = dfall[np.isclose(dfall['massFlowRate_sccm'],108.75)]

# Plot curve for each sheath voltage
for phis in np.unique(dfx['sheathVoltage']):
    dfxx = dfx[dfx['sheathVoltage'] == phis]
    Idvec = np.array(dfxx['dischargeCurrent'])
    Pvec = np.array(dfxx['totalPressureCorr_Torr'])
    ax.plot(Idvec,Pvec)


#### Experimental data
xp_constant_mdot = np.array([[100, 2.44 ,0.0061],                                                                                   
[159, 3.11, 0.007775],                                                      
[200, 3.63 ,0.009075],                                                    
[250.67,4.3, 0.01075],               
[306.67, 5.4 ,0.0135]])
ax.errorbar(xp_constant_mdot[:,0],xp_constant_mdot[:,1],yerr = xp_constant_mdot[:,2],fmt='ko')
    
### Labels
ax.set_xlabel('Discharge current (A)')
ax.set_ylabel('Total pressure (Torr)')
ax.set_title("mdot = 109 sccm")

