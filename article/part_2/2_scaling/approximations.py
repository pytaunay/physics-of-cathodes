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
File: approximations.py
Author: Pierre-Yves Taunay
Date: February, 2022 

Description: generate Fig. 3 and 4 in Part 2 of Physics of Thermionic Orificed Hollow Cathodes.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cathode.constants as cc

from cathode.models.taunay_et_al_core.correlation import Te_insert
from cathode.models.taunay_et_al_core.collision_holder import collision_holder

### Recreate Figure 3
Pd = np.logspace(-1,1,20)

for sp in ['Ar','Xe']:
    ### Create a collision holder
    chold = collision_holder(sp)

    ng = Pd*cc.Torr / (cc.kB * 3000) # Density 
    ds = 1.0e-2 # 1 cm, arbitrary
    Te = Te_insert(ng,ds,sp) # Electron temp, eV

    xsec = chold.xsec('iz',Te) # Maxwellian-averaged cross section

    plt.loglog(Pd,xsec*np.sqrt(Te)*np.sqrt(8.0*cc.e*Te/(np.pi*cc.me)),'k-')

    if sp == 'Xe':
        plt.loglog(Pd,0.5e-16/(Pd)**2,'k--')
        plt.annotate('Xe',xy=(0.5,5e-17))
    else:
        plt.loglog(Pd,2e-16/(Pd)**2,'k--')
        plt.annotate('Ar',xy=(2,1e-16))

plt.xlabel("Pressure-diameter (Torr-cm)")
plt.ylabel("<sigma_iz v> Te^{1/2}")


### Recreate Figure 4
fig, ax = plt.subplots(3,2)

### Path to HDF5 file
hdf5_paths = [
        '../../../results/nstar.h5',
        '../../../results/jpl_lab6.h5'
        ]

key_root = 'Xe/simulations/results/'

end_keys = [
        ['r20210304223500','r20210304225118','r20210304230806'], # NSTAR
        ['r20210303211954','r20210303213415','r20210303214842'], # JPL LaB6
        ]

mass_flow_rates = [
        3.7,
        12.0
        ]

Tgvec = [2000,3000,4000]

ax_idx = 0
for path_to_results, key_end, mdot_sccm in zip(hdf5_paths,end_keys,mass_flow_rates):
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

    ### Get data for specified mass flow rate in sccm 
    dfx = dfall[np.isclose(dfall['massFlowRate_sccm'],mdot_sccm)]

    Idvec = np.unique(dfx['dischargeCurrent'])
    alpha_i = np.zeros_like(Idvec)
    ne_o = np.zeros_like(Idvec)
    sqrt_t = np.zeros_like(Idvec)

    for kk, Id in enumerate(Idvec):
        dfxx = dfx[dfx['dischargeCurrent'] == Id]
        alpha_i[kk] = np.nanmean(dfxx['insertIonizationFraction'])
        ne_o[kk] = np.nanmean(dfxx['orificeNeutralDensity'])

        alpha_o = (dfxx['orificeIonizationFraction'])
        Tn = (dfxx['neutralGasTemperature'])
        Te = (dfxx['orificeElectronTemperature'] * cc.eV2Kelvin)
        sqrt_t[kk] = np.sqrt(np.nanmean((1 + alpha_o * Te/Tn)))
        print(alpha_o)

    ax[0][ax_idx].plot(Idvec,alpha_i,'k-')
    ax[1][ax_idx].plot(Idvec,ne_o,'k-')
    ax[2][ax_idx].plot(Idvec,sqrt_t,'k-')


    # Approximations
    a,b = np.polyfit(np.log10(Idvec),np.log10(alpha_i),1)
    ax[0][ax_idx].plot(Idvec,10**b * Idvec**a,'k--')

    a,b = np.polyfit(Idvec,ne_o,1)
    ax[1][ax_idx].plot(Idvec,a*Idvec + b,'k--')

    a,b,c = np.polyfit(Idvec,sqrt_t,2)
    ax[2][ax_idx].plot(Idvec,a*Idvec**2 + b*Idvec + c,'k--')



    ax_idx = ax_idx + 1


ax[0][0].set_title("NSTAR cathode")
ax[0][1].set_title("JPL 1.5 cathode")
ax[0][0].set_ylabel("Insert ionization fraction")
ax[1][0].set_ylabel("Orifice neutral density (1/m3)")
ax[2][0].set_ylabel("sqrt( 1 + alpha_o * Te_o / Tn)")

ax[2][0].set_xlabel("Discharge current (A)")
ax[2][1].set_xlabel("Discharge current (A)")

plt.show()
