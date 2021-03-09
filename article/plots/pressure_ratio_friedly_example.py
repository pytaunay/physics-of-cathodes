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
File: pressure_ratio_friedly_example.py
Author: Pierre-Yves Taunay
Date: March, 2021
Description: generates Fig. 2a in Part 2 of Physics of Thermionic Orificed Hollow Cathodes.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### Path to HDF5 file
path_to_results = '../../results/friedly.h5'

### Generate a dataframe out of results for the following parameters:
# Discharge current = 5-60 A
# Mass flow rate = 0.37 eqA (5.16 sccm)
# Neutral gas temperature = 2000, 3000, 4000 K
# Sheath voltage = 1-10 V
key_root = 'Xe/simulations/results/'
key_end = ['r20210306023131','r20210306174156','r20210306180132']
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
md = np.unique(dfall['massFlowRate_eqA'])[0]

min_ratio = np.zeros_like(Idvec)
max_ratio = np.zeros_like(Idvec)

for kk, Id in enumerate(Idvec):
    dfx = dfall[dfall['dischargeCurrent'] == Id]
    
    min_ratio[kk] = np.min(dfx['totalPressure']/dfx['magneticPressure'])
    max_ratio[kk] = np.max(dfx['totalPressure']/dfx['magneticPressure'])

# Plot results
plt.loglog(Idvec/md,min_ratio,'k-')
plt.loglog(Idvec/md,max_ratio,'k-')
plt.fill_between(Idvec/md,min_ratio,max_ratio,color=(0.5,0.5,0.5,0.5))
#
## Plot experimental data
xp_data = np.array([
[13.5060666036119,95.6270431300905],
[27.0121332072238,37.3136722293613],
[40.5181998108357,20.824230636672],
[54.0242664144477,14.3747937333768],
[67.5303330180596,10.991317693348],
[81.0363996216715,8.85658208341987],
[94.5424662252834,7.1052844617966],
[108.048532828895,5.96712749131765],
[121.554599432507,5.12223642383175],
[135.060666036119,4.4641982374605],
[148.566732639731,3.8707840003619],
[162.072799243343,3.47665017360819],
])

plt.plot(xp_data[:,0],xp_data[:,1],'ko')


# Plot labels and limits
plt.xlim([10,200])
plt.ylim([1,300])

plt.xlabel("Id / mdot")
plt.ylabel("P / Pmag")
