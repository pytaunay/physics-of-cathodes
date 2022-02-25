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
File: pressure_ratio_plhc_example.py
Author: Pierre-Yves Taunay
Date: March, 2021
Description: generates Fig. 2e in Part 2 of Physics of Thermionic Orificed Hollow Cathodes.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### Path to HDF5 file
path_to_results = '../../results/plhc.h5'

### Generate a dataframe out of results for the following parameters:
# Discharge current = 100-307 A
# Mass flow rate = 0.37 eqA (5.16 sccm)
# Neutral gas temperature = 2000, 3000, 4000 K
# Sheath voltage = 1-10 V
key_root = 'Ar/simulations/results/'
key_end = ['r20210309170903','r20210309173700','r20210309180518']
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
    
    min_ratio[kk] = np.min(dfx['totalPressureCorr']/dfx['magneticPressure'])
    max_ratio[kk] = np.max(dfx['totalPressureCorr']/dfx['magneticPressure'])

# Plot results
plt.loglog(Idvec/md,min_ratio,'k-')
plt.loglog(Idvec/md,max_ratio,'k-')
plt.fill_between(Idvec/md,min_ratio,max_ratio,color=(0.5,0.5,0.5,0.5))
#
## Plot experimental data
xp_data = np.array([
[12.8167914804,4.35777848414,0.0108944462104,0.0108944462104],
[20.3786984538,2.19705770836,0.00549264427089,0.00549264427089],
[25.6335829608,1.62077212064,0.0040519303016,0.0040519303016],
[32.1278512039,1.22219093288,0.0030554773322,0.0030554773322],
[39.3052544329,1.02547835343,0.00256369588359,0.00256369588359],
])

plt.plot(xp_data[:,0],xp_data[:,1],'ko')


## Plot labels and limits
plt.xlim([10,100])
plt.ylim([1,10])

plt.xlabel("Id / mdot")
plt.ylabel("P / Pmag")

plt.show()
