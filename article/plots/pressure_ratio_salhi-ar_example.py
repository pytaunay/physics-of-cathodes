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
File: pressure_ratio_salhi-ar_example.py
Author: Pierre-Yves Taunay
Date: March, 2021
Description: generates Fig. 2d in Part 2 of Physics of Thermionic Orificed Hollow Cathodes.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

### Find the minimum and maximum bounds for each discharge current
for idx,md in enumerate(np.unique(dfall['massFlowRate_eqA'])):
    dfx = dfall[dfall['massFlowRate_eqA']==md]
    Idvec = np.unique(dfx['dischargeCurrent'])
    
    min_ratio = np.zeros_like(Idvec)
    max_ratio = np.zeros_like(Idvec)
    
    for kk, Id in enumerate(Idvec):
        dfxx = dfx[dfx['dischargeCurrent'] == Id]
        
        min_ratio[kk] = np.nanmin(dfxx['totalPressureCorr']/dfxx['magneticPressure'])
        max_ratio[kk] = np.nanmax(dfxx['totalPressureCorr']/dfxx['magneticPressure'])
    
    # Plot results
    plt.loglog(Idvec/md,min_ratio,'k-')
    plt.loglog(Idvec/md,max_ratio,'k-')
    plt.fill_between(Idvec/md,min_ratio,max_ratio,color=(0.5,0.5,0.5,0.5))

    ## Plot experimental data
    if idx == 0:
        xp_data = np.array([
            [2,5316.34861111339],
            [4,1359.01870574937],
            [6,635.710946408889],
            [8,367.566877926228],
            [10,239.799201797101],
            [14,127.815608942121],
            [18,79.5695437435862],
            [24,46.0617915438062],
            [28,34.5960578776159],
            [30,30.4911044389275],
            [40,18.8760828511939],
        ])
    else:
        xp_data = np.array([
            [2.1505376344086,2174.93473265882],
            [3.2258064516129,976.57521499222],
            [4.3010752688172,551.230288892781],
            [5.3763440860215,358.726507336079],
            [6.45161290322581,254.060021470301],
            [7.52688172043011,189.686506817313],
            [8.60215053763441,146.166664840847],
            [9.67741935483871,117.322772974465],
            [10.752688172043,95.3354255840365],
            [11.8279569892473,80.0166993348854],
            [12.9032258064516,67.2431130448907],
            [13.9784946236559,58.8731742794513],
            [16.1290322580645,44.7528995777509],
        ])
    
    plt.plot(xp_data[:,0],xp_data[:,1],'ko')


# Plot labels and limits
plt.xlim([1,100])
plt.ylim([10,1e4])

plt.xlabel("Id / mdot")
plt.ylabel("P / Pmag")
