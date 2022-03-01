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
File: pressure-budget.py
Author: Pierre-Yves Taunay
Date: February, 2022 
Description: generate Fig. 5 in Part 2 of Physics of Thermionic Orificed Hollow Cathodes.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### Path to HDF5 file
hdf5_paths = [
        '../../../results/siegfried.h5',
        '../../../results/nstar.h5',
        '../../../results/jpl_lab6.h5',
        '../../../results/plhc.h5'
        ]

root_keys = [
        'Xe/simulations/results/',
        'Xe/simulations/results/',
        'Xe/simulations/results/',
        'Ar/simulations/results/',
        ]

end_keys = [
        ['r20210305021601','r20210305022632','r20210305023703'], # Siegfried and Wilbur
        ['r20210304223500','r20210304225118','r20210304230806'], # NSTAR
        ['r20210303211954','r20210303213415','r20210303214842'], # JPL LaB6
        ['r20210309170903','r20210309173700','r20210309180518'], # PLHC
        ]

mass_flow_rates = [
        0.0,
        3.7,
        12.0,
        108.75 
        ]

fig, ax = plt.subplots(2,2)


cat_idx = 0
i_plt_idx = 0
j_plt_idx = 0

Tgvec = [2000,3000,4000]
for path_to_results, key_root, key_end, mdot_sccm in zip(hdf5_paths,root_keys,end_keys,
        mass_flow_rates):
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

    ### Get data
    if cat_idx == 0:
        dfx = dfall[np.isclose(dfall['dischargeCurrent'],2.3)]
        dfxx = dfx
        Idvec = np.array(dfxx['massFlowRate_sccm'])
        Idvec = np.unique(Idvec)
    else:
        dfx = dfall[np.isclose(dfall['massFlowRate_sccm'],mdot_sccm)]
        dfxx = dfx
        Idvec = np.array(dfxx['dischargeCurrent'])
        Idvec = np.unique(Idvec)


    rgd_arr = []
    rmf_arr = []
    rma_arr = []
    for Id in np.unique(Idvec): 
        if cat_idx == 0:
            dfxxx = dfxx[np.isclose(dfxx.massFlowRate_sccm, Id,1e-2)]
        else:
            dfxxx = dfxx[dfxx.dischargeCurrent == Id]

        rgd = (dfxxx['gasdynamicPressure']+dfxxx['exitStaticPressure'])/dfxxx['totalPressure']
        rmf = dfxxx['momentumFluxPressure']/dfxxx['totalPressure']
        rmag = dfxxx['magneticPressure']/dfxxx['totalPressure']
        
        rgd_arr.append(np.nanmean(rgd))
        rmf_arr.append(np.nanmean(rmf))
        rma_arr.append(np.nanmean(rmag))

    rgd_arr = np.array(rgd_arr)
    rmf_arr = np.array(rmf_arr)
    rma_arr = np.array(rma_arr)
    
        
    #    print(rgd_arr,rmf_arr,rma_arr)    
    ax[i_plt_idx][j_plt_idx].plot(Idvec,rgd_arr,'k-')
    ax[i_plt_idx][j_plt_idx].plot(Idvec,rmf_arr,'k--')
    ax[i_plt_idx][j_plt_idx].plot(Idvec,rma_arr,'k-.')
    if cat_idx == 0:
        ax[i_plt_idx][j_plt_idx].set_xlabel("Mass flow rate (sccm Xe)")
        cat_idx = 1
    else:
        ax[i_plt_idx][j_plt_idx].set_xlabel("Discharge current (A)")
    ax[i_plt_idx][j_plt_idx].set_ylabel("Pressure budget")

    j_plt_idx = j_plt_idx + 1
    if j_plt_idx >= 2:
        i_plt_idx = i_plt_idx + 1
        j_plt_idx = 0


ax[0][0].legend(['Gasdynamic','Momentum flux','Magnetic'])
ax[0][0].set_title("Siegfried and Wilbur (Id = 2.3 A)")
ax[0][1].set_title("NSTAR (3.7 sccm of Xe)")
ax[1][0].set_title("JPL 1.5 cm cathode (12.0 sccm of Xe)")
ax[1][1].set_title("PLHC (109 sccm of Ar)")

plt.show()
