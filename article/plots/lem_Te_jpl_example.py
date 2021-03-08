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
File: lem_Te_jpl_example.py
Author: Pierre-Yves Taunay
Date: March, 2021
Description: generate Fig. 12a and 12b in Part 1 of Physics of Thermionic Orificed Hollow Cathodes.
We only consider the JPL LaB6 cathode for this example.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### Path to HDF5 file
path_to_results = '../results/jpl_lab6.h5'

### Generate a dataframe out of results for the following parameters:
# Discharge current = 20-100 A
# Mass flow rate = 8 sccm, 12 sccm
# Neutral gas temperature = 2000 - 4000 K
# Sheath voltage = 1-10 V
key_root = 'Xe/simulations/results/'
key_end = ['r20210303211954','r20210303213415','r20210303214842']
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

# Plot the bounds and fill the area for each mass flow rate
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
        
        min_te[kk] = np.min(dfxx['insertElectronTemperature'])
        max_te[kk] = np.max(dfxx['insertElectronTemperature'])

        min_lem[kk] = np.min(dfxx['emissionLength'])/dc
        max_lem[kk] = np.max(dfxx['emissionLength'])/dc
    
    # Plot
    ax[0].fill_between(Idvec,min_lem,max_lem,color=color)
    ax[0].plot(Idvec,min_lem,style)
    ax[0].plot(Idvec,max_lem,style)
    
    ax[1].fill_between(Idvec,min_te,max_te,color=color)
    ax[1].plot(Idvec,min_te,style)
    ax[1].plot(Idvec,max_te,style)
    
### Experimental data
xp_lem_8sccm = np.array([
[20.0,0.58720030212,0.116664079989],
[30.0,0.533589413381,0.132413703393],
[40.0,0.67429445503,0.152640573619],
[50.0,0.60740023117,0.132866138551],
[60.0,0.62992468652,0.13449416021],
[70.0,0.573557995218,0.124295484781],
[80.0,0.573657258458,0.117647574019],
[90.0,0.477010349112,0.151869201954],
[100.0,0.428181145236,0.0710545228643]
])

xp_lem_12sccm = np.array([
[20.0,0.436996003135,0.0501554027827],
[30.0,0.407687660772,0.0698057014419],
[40.0,0.408506452306,0.0896716963446],
[50.0,0.421746067047,0.113291160418],
[60.0,0.364722366088,0.166748276153],
[70.0,0.372709013714,0.0847913232138],
[80.0,0.430226686184,0.0626863105143],
[90.0,0.407620207491,0.0551688232317],
[100.0,0.428089621117,0.0620896520614],
])

ax[0].errorbar(xp_lem_8sccm[:,0], xp_lem_8sccm[:,1], yerr=xp_lem_8sccm[:,2], fmt='ks')
ax[0].errorbar(xp_lem_12sccm[:,0], xp_lem_12sccm[:,1], yerr=xp_lem_12sccm[:,2], fmt='k^')

xp_te_8sccm = np.array([
[20,2.26648,0.5],
[30,2.25549,0.5],
[40,2.2033,0.5],
[50,1.7838716696245,0.5],
[60,2.1978,0.5],
[70,2.17033,0.5],
[80,2.09615,0.5],
[100,1.98345050689552,0.5],
[90,2.13736,0.5],
])

xp_te_12sccm = np.array([
[20,1.73626,0.5],
[30,1.79121,0.5],
[40,1.68132,0.5],
[50,1.5476210306236,0.5],
[90,1.57418,0.5],
[60,1.45055,0.5],
[70,1.6978,0.5],
[80,1.60989,0.5],
[100,1.69163582541647,0.5],
])

ax[1].errorbar(xp_te_8sccm[:,0], xp_te_8sccm[:,1], yerr=xp_te_8sccm[:,2], fmt='ks')
ax[1].errorbar(xp_te_12sccm[:,0], xp_te_12sccm[:,1], yerr=xp_te_12sccm[:,2], fmt='k^')

### Labels
ax[0].set_xlabel('Discharge current (A)')
ax[0].set_ylabel('Emission length / insert diameter')
ax[1].set_ylim([0,1])

ax[1].set_xlabel('Discharge current (A)')
ax[1].set_ylabel('Insert electron temperature (eV)')
ax[1].set_ylim([0,3])
