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
File: lem_Te_salhi_example.py
Author: Pierre-Yves Taunay
Date: March, 2021
Description: generate Fig. 13a and 13b in Part 1 of Physics of Thermionic Orificed Hollow Cathodes.
We only consider Salhi's cathode for this example.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### Path to HDF5 file
path_to_results = '../../../results/salhi_xe.h5'

### Generate a dataframe out of results for the following parameters:
# Discharge current = 1-20 A
# Mass flow rate = 0.5 eqA (6 sccm)
# Neutral gas temperature = 2000 - 4000 K
# Sheath voltage = 1-10 V
key_root = 'Xe/simulations/results/'
key_end = ['r20210304172101','r20210304172637','r20210304173212']
Tgvec = [2000,3000,4000]

# Create a list for each dataframe
dlist = []
for TgK, ke in zip(Tgvec,key_end):
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

### Find the minimum and maximum bounds for each discharge current
Idvec = np.unique(dfall['dischargeCurrent'])
mdvec = np.unique(dfall['massFlowRate_sccm'])
dc = np.unique(dfall['insertDiameter'])

min_lem = np.zeros_like(Idvec)
max_lem = np.zeros_like(Idvec)

min_te = np.zeros_like(Idvec)
max_te = np.zeros_like(Idvec)

# Plot the bounds and fill the area for each mass flow rate (there is only one here)
for idx, md in enumerate(mdvec):
    dfx = dfall[dfall['massFlowRate_sccm'] == md]
    
    # Change color and style depending on the mass flow
    if idx == 0:
        style = 'k--'
        color = (0.7,0.7,0.7,0.5)
    else:
        style = 'k-.'
        color = (0.1,0.1,0.1,0.5)
    
    # Populate vectors to plot
    for kk, Id in enumerate(Idvec):
        dfxx = dfx[dfx['dischargeCurrent'] == Id]
        
        min_te[kk] = np.nanmin(dfxx['insertElectronTemperature'])
        max_te[kk] = np.nanmax(dfxx['insertElectronTemperature'])

        min_lem[kk] = np.nanmin(dfxx['emissionLength'])/dc
        max_lem[kk] = np.nanmax(dfxx['emissionLength'])/dc
    
    # Plot
    ax[0].fill_between(Idvec,min_lem,max_lem,color=color)
    ax[0].plot(Idvec,min_lem,style,label='_nolegend_')
    ax[0].plot(Idvec,max_lem,style,label='_nolegend_')
    
    ax[1].fill_between(Idvec,min_te,max_te,color=color)
    ax[1].plot(Idvec,min_te,style,label='_nolegend_')
    ax[1].plot(Idvec,max_te,style,label='_nolegend_')

### Experimental data
xp_lem = np.array([
[5.0,0.344379987000234,0.0813386106947],
[9.0,0.31421574796719,0.0742309185405],
[12.0,0.282429429616658,0.0668072441952],
[15,0.439504506861141,0.127464586651],
])

ax[0].errorbar(xp_lem[:,0], xp_lem[:,1], yerr=xp_lem[:,2], fmt='ks')

xp_te = np.array([
[3,1.00,0.1,],
[5,1.11301642931159,0.5],
[9,1.08529116781942,0.5],
[10,0.98,0.12,],
[15,0.966499173349343,0.5],
[20,1.07,0.15],
])

ax[1].errorbar(xp_te[:,0], xp_te[:,1], yerr=xp_te[:,2], fmt='ks')
    

### Labels
ax[0].set_title("Salhi's cathode attachment length")
ax[1].set_title("Salhi's cathode electron temperature")
ax[0].legend(['This work','Experiment'])
ax[1].legend(['This work','Experiment'])

ax[0].set_xlabel('Discharge current (A)')
ax[0].set_ylabel('Emission length / insert diameter')
ax[0].set_ylim([0,1])
ax[0].set_xlim([1,25])

ax[1].set_xlabel('Discharge current (A)')
ax[1].set_ylabel('Insert electron temperature (eV)')
ax[1].set_ylim([0,3])
ax[1].set_xlim([1,25])

plt.show()
