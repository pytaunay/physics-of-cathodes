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
File: pressure_nstar_example.py
Author: Pierre-Yves Taunay
Date: March, 2021
Description: generate Fig. 13a and 13b in Part 1 of Physics of Thermionic Orificed Hollow Cathodes.
The data presented are for a neutral gas temperature of 3000 K
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### Path to HDF5 file
path_to_results = '../../results/nstar.h5'

### Generate a dataframe out of results for the following parameters:
# Discharge current = 5-15 A; 12 A
# Mass flow rate = 3.7 sccm; 4-6 sccm
# Neutral gas temperature = 3000 K
# Sheath voltage = 1-10 V
key_root = 'Xe/simulations/results/'
key_end = ['r20210304225118','r20210305144515']
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

fig, ax = plt.subplots(1,2)

### Get data for mass flow of 3.7 sccm
dfx = dfall[np.isclose(dfall['massFlowRate_sccm'],3.7)]

# Plot curve for each sheath voltage
for phis in np.unique(dfx['sheathVoltage']):
    dfxx = dfx[dfx['sheathVoltage'] == phis]
    
    Idvec = np.array(dfxx['dischargeCurrent'])
    Pvec = np.array(dfxx['totalPressureCorr_Torr'])
    ax[0].plot(Idvec,Pvec)
    
### Get data for discharge current of 12 A
dfx = dfall[np.isclose(dfall['dischargeCurrent'],12.)]

# Plot curve for each sheath voltage
for phis in np.unique(dfx['sheathVoltage']):
    dfxx = dfx[dfx['sheathVoltage'] == phis]
    dfxx = dfxx[dfxx['massFlowRate_sccm'] <= 5.0]
    
    mdvec = np.array(dfxx['massFlowRate_sccm'])
    Pvec = np.array(dfxx['totalPressureCorr_Torr'])
    ax[1].plot(mdvec,Pvec)

### Experimental data
xp_constant_mdot = np.array([[13.2, 8.0824],                                                                                      
[13, 7.6651],                                                        
[6, 7.0818],                                                                                         
[8, 7.3746],                                                                                          
[10, 8.3778],                                                                                          
[12, 9.5007],                                                                                         
[15, 11.8545]])
ax[0].plot(xp_constant_mdot[:,0],xp_constant_mdot[:,1],'ko')

    
xp_constant_id = np.array([[3.0, 6.5039],                                                                                          
[3.25, 7.0642],                                                                      
[3.5, 7.5596],                                                                                       
[3.75, 7.4458],                                                                                        
[4, 7.9005],                                                                                       
[4.25, 8.4528],                                                                                         
[4.5, 8.6801],                                                                                       
[4.75, 9.0455],                                                                                        
[5, 9.4272],                                                                                       
[3.7, 9.5007]])

ax[1].plot(xp_constant_id[:,0],xp_constant_id[:,1],'ko')
    
### Labels
ax[0].set_xlabel('Discharge current (A)')
ax[0].set_ylabel('Total pressure (Torr)')
ax[0].set_title("mdot = 3.7 sccm")

ax[1].set_xlabel('Mass flow rate (sccm)')
ax[1].set_ylabel('Total pressure (Torr)')
ax[1].set_title("Id = 12 A")

