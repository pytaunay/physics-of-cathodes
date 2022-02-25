# MIT License
# 
# Copyright (c) 2022 Pierre-Yves Camille Regis Taunay
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
File: pressure_nexis_example.py
Author: Pierre-Yves Taunay
Date: February, 2022
Description: generate Fig. 14c and 14d in Part 1 of Physics of Thermionic Orificed Hollow Cathodes.
The data presented are for a neutral gas temperature of 3000 K
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### Path to HDF5 file
path_to_results = '../../../results/nexis.h5'

### Generate a dataframe out of results for the following parameters:
# Discharge current = 8-26 A; 22 A
# Mass flow rate = 5.5 sccm; 4-10 sccm
# Neutral gas temperature = 3000 K
# Sheath voltage = 1-10 V
key_root = 'Xe/simulations/results/'
key_end = ['r20210305164507','r20210305174356']
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

### Get data for mass flow of 5.5 sccm
dfx = dfall[np.isclose(dfall['massFlowRate_sccm'],5.5)]

# Plot curve for each sheath voltage
for phis in np.unique(dfx['sheathVoltage']):
    dfxx = dfx[dfx['sheathVoltage'] == phis]
    
    Idvec = np.array(dfxx['dischargeCurrent'])
    Pvec = np.array(dfxx['totalPressureCorr_Torr'])
    ax[0].plot(Idvec,Pvec)
    
### Get data for discharge current of 12 A
dfx = dfall[np.isclose(dfall['dischargeCurrent'],22.)]

# Plot curve for each sheath voltage
for phis in np.unique(dfx['sheathVoltage']):
    dfxx = dfx[dfx['sheathVoltage'] == phis]
    dfxx = dfxx[dfxx['massFlowRate_sccm'] <= 10.0]
    
    mdvec = np.array(dfxx['massFlowRate_sccm'])
    Pvec = np.array(dfxx['totalPressureCorr_Torr'])
    ax[1].plot(mdvec,Pvec)

### Experimental data
xp_constant_mdot = np.array([
[8,1.11388],
[10,1.18253],
[12,1.29485],
[14,1.35413],
[16,1.3947],
[18,1.42278],
[20,1.45398],
[22,1.54134],
[24,1.60686],
[26,1.67863],
[22,1.43977],
])
ax[0].plot(xp_constant_mdot[:,0],xp_constant_mdot[:,1],'ko')

    
xp_constant_id = np.array([
[5.5,1.54134],
[4,1.25],
[5.5,1.43977],
[7,1.85228],
[10,2.75909],
[5,1.01284],
])

ax[1].plot(xp_constant_id[:,0],xp_constant_id[:,1],'ko')
    
### Labels
ax[0].legend(["phi_sheath = 1 V","4 V","7 V","10 V","Experiment"])
ax[1].legend(["phi_sheath = 1 V","4 V","7 V","10 V","Experiment"])

ax[0].set_xlabel('Discharge current (A)')
ax[0].set_ylabel('Total pressure (Torr)')
ax[0].set_title("NEXIS, mdot = 5.5 sccm")

ax[1].set_xlabel('Mass flow rate (sccm of Xe)')
ax[1].set_ylabel('Total pressure (Torr)')
ax[1].set_title("NEXIS, Id = 22 A")

plt.show()
