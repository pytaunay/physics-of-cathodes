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
File: twall_salhi_example.py
Author: Pierre-Yves Taunay
Date: March, 2021
Description: generate Fig. 11b in Part 1 of Physics of Thermionic Orificed Hollow Cathodes.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cathode.constants as cc
from scipy.optimize import root
from cathode.models.taunay_et_al_core.collision_holder import collision_holder

### Path to HDF5 file
path_to_results = '../../results/salhi_ar.h5'

### Generate a dataframe out of results for the following parameters:
# Discharge current = 1-20 A
# Mass flow rate = 0.5, 0.93 A
# Neutral gas temperature = 2000, 3000, 4000 K
# Sheath voltage = 1-10 V
key_root = 'Ar/simulations/results/'
key_end = ['r20210309170114','r20210309180313','r20210309190430']
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
dfall.reset_index(inplace=True)
dfx = dfall.dropna() # Drop NaN's to avoid issues when computing wall temperature

### Create a collision holder
chold = collision_holder('Ar')

### For Salhi's argon cathode we must recompute the wall temperature because the code only considers
### Ba-O for now. We also consider two constant work functions for Salhi's cathode (1.8 and 2.0 eV)
RDConstant = 120e4
for wf in [1.8, 2.0]:
    phi_wf = lambda Tw: wf # Constant work function
    
    for index, row in dfx.iterrows():
        ### Unpack data
        dc = row['insertDiameter']
        Lem_i = row['emissionLength']
        phi_s = row['sheathVoltage']
        Te_i = row['insertElectronTemperature']
        M = row['mass']
        al_i = row['insertIonizationFraction']
        ng_i = row['insertNeutralDensity']
        Id = row['dischargeCurrent']
    
        #### Solve for the wall temperature     
        V_i = np.pi * Lem_i * (dc/2)**2
        f_Ir = 1/4 * np.sqrt(8*M/(np.pi*cc.me)) * np.exp(-phi_s/Te_i)
        f_Ii = 1
        
        rhs = al_i / (1-al_i) * ng_i**2 * cc.e * chold.xsec('iz',Te_i) * V_i
        rhs *= (f_Ir-f_Ii)
        rhs += Id
        
        rhs /= (np.pi * Lem_i * dc * RDConstant)
        lhs = lambda Tw: Tw**2 * np.exp(-cc.e*(phi_wf(Tw))/(cc.kB*Tw))
 
        
        # Solve    
        sol = root(lambda Tw: lhs(Tw)-rhs,1500)
        Tw = sol.x[0] - 273.15 # to degC
        
        # Update the corresponding quantity
        dfx.loc[index,'insertTemperature'] = Tw

    ### Now, for each discharge current, compute minimum / maximum wall temperature, then display
    Idvec = np.unique(dfall['dischargeCurrent'])
    minTw = np.zeros_like(Idvec)
    maxTw = np.zeros_like(Idvec)
    
    for kk,Id in enumerate(Idvec):
        dfxx = dfx[dfx['dischargeCurrent'] == Id]
        
        minTw[kk] = np.min(dfxx['insertTemperature'])
        maxTw[kk] = np.max(dfxx['insertTemperature'])    
    
    ### Plot data
    plt.plot(Idvec,minTw)
    plt.plot(Idvec,maxTw)
    plt.fill_between(Idvec,minTw,maxTw)
    
xp_6sccm = np.array([
[5,933.067,15],
[7,974.13,15,],
[9,1013.473,15],
[12,1059.572,15],
[14,1087.718,15],
[15,1098.779,15],
])
    
xp_13sccm = np.array([
[2,871.997,15],
[3,910.251,15],
[5,957.939,15],
[7,989.373,15],
[8,996.594,15],
[10,1026.55,15],
[13,1064.456,15],
])
    
plt.errorbar(xp_6sccm[:,0], xp_6sccm[:,1], yerr=xp_6sccm[:,2],fmt='ko')
plt.errorbar(xp_13sccm[:,0], xp_13sccm[:,1], yerr=xp_13sccm[:,2],fmt='k^')

plt.xlim([0,21])
plt.ylim([100,1300])

