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
File: twall_nstar_example.py
Author: Pierre-Yves Taunay
Date: March, 2021
Description: generate Fig. 11a in Part 1 of Physics of Thermionic Orificed Hollow Cathodes.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### Path to HDF5 file
path_to_results = '../../results/nstar.h5'

### Generate a dataframe out of results for the following parameters:
# Discharge current = 5-15 A
# Mass flow rate = 3.7 sccm, 10 sccm
# Neutral gas temperature = 2000, 3000, 4000 K
# Sheath voltage = 1-10 V
key_root = 'Xe/simulations/results/'
key_end = ['r20210304223500','r20210304225118','r20210304230806']
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
Idvec = np.unique(dfall['dischargeCurrent'])
minTw = np.zeros_like(Idvec)
maxTw = np.zeros_like(Idvec)

for kk, Id in enumerate(Idvec):
    dfx = dfall[dfall['dischargeCurrent'] == Id]
    
    minTw[kk] = np.min(dfx['insertTemperature'])
    maxTw[kk] = np.max(dfx['insertTemperature'])

# Plot results
plt.plot(Idvec,minTw,'k-')
plt.plot(Idvec,maxTw,'k-')

# Plot experimental data
# 3.7 sccm
xp_low_massflow = np.array([[13.2,1264.4493932429],
[13,1262.13178637046], 
[6,1105.645],
[8,1151.224],
[10,1189.693],
[12,1206.733],
[15,1238.492]])

plt.errorbar(xp_low_massflow[:,0],xp_low_massflow[:,1],yerr=15,fmt='ko')

# 10 sccm
xp_high_massflow = np.array([[6,1109.596],
[8,1170.134],
[10,1208.071]])
plt.errorbar(xp_high_massflow[:,0],xp_high_massflow[:,1],yerr=15,fmt='k^')


# Plot labels and limits
plt.ylim([100,np.max(maxTw)+100])
plt.xlim([4,16])
plt.xlabel("Discharge current")
plt.ylabel("Insert wall temperature (degC)")

plt.show()
