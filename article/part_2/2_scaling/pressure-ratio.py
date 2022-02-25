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
File: pressure-ratio.py
Author: Pierre-Yves Taunay
Date: February, 2022 

Description: generate Fig. 2 in Part 2 of Physics of Thermionic Orificed Hollow Cathodes.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Path to HDF5 files
hdf5_paths = [
        '../../../results/friedly.h5',
        '../../../results/nstar.h5',
        '../../../results/nexis.h5',
        '../../../results/salhi_ar.h5',
        '../../../results/plhc.h5']

root_keys = [
        'Xe/simulations/results/',
        'Xe/simulations/results/',
        'Xe/simulations/results/',
        'Ar/simulations/results/',
        'Ar/simulations/results/',
        ]

end_keys = [
        ['r20210306023131','r20210306174156','r20210306180132'], # Friedly
        ['r20210304223500','r20210304225118','r20210304230806'], # NSTAR
        ['r20210305163012','r20210305164507','r20210305170023'], # NEXIS 
        ['r20210309170114','r20210309180313','r20210309190430'], # Salhi-Ar
        ['r20210309170903','r20210309173700','r20210309180518'], # PLHC
        ]

# xylims
xylims = [
        np.array([[10.,200.],[1.0,200.0]]),
        np.array([[1.,100.],[10.0,600.]]),
        np.array([[10.,100.],[1.0,200.]]),
        np.array([[1.,100.],[10.0,1e4]]),
        np.array([[10.,100.],[1.0,10.0]]),
        ]

# Experimental data
xp_data_all = [
        # Friedly
    np.array([
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
    ]),
        # NSTAR
[np.array([
[8.3629564409565,411.653371191889],
[11.150608587942,265.063110180467],
[13.9382607349275,191.122456641961]
]),
np.array([
[49.7256869462278,32.28615417983],
[48.9722674470425,31.5685736136439],
[22.6025849755581,136.919402589118],
[30.1367799674108,80.2014709978693],
[37.6709749592635,58.311448157813],
[45.2051699511162,45.9215936689271],
[56.5064624388952,36.6711527124222],
    ])
    ],
        # NEXIS
        np.array([
            [20.273834,60.737651],
            [25.342292,41.267839],
            [30.410751,31.380259],
            [35.479209,24.110368],
            [40.547668,19.012551],
            [45.616126,15.324711],
            [50.684584,12.685220],
            [55.753043,10.381194],
            [55.753043,11.113546],
            [60.821501,9.735429],
            [65.889960,8.665784],
            ]),
        # Salhi
    [np.array([
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
        ]),
    np.array([
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
        ])],
        np.array([
        [12.8167914804,4.35777848414,0.0108944462104,0.0108944462104],
        [20.3786984538,2.19705770836,0.00549264427089,0.00549264427089],
        [25.6335829608,1.62077212064,0.0040519303016,0.0040519303016],
        [32.1278512039,1.22219093288,0.0030554773322,0.0030554773322],
        [39.3052544329,1.02547835343,0.00256369588359,0.00256369588359],
        ])
        ]
   

Tgvec = [2000,3000,4000]

fig, ax = plt.subplots(3,2)

idx_i = 0
idx_j = 0

for path_to_results, key_root, key_end, lims, xp_data in zip(hdf5_paths,root_keys,end_keys,xylims,
        xp_data_all): 
    ### Generate a dataframe out of results for the following parameters:
    # Discharge current = 5-60 A
    # Mass flow rate = 0.37 eqA (5.16 sccm)
    # Neutral gas temperature = 2000, 3000, 4000 K
    # Sheath voltage = 1-10 V
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
        ax[idx_i][idx_j].loglog(Idvec/md,min_ratio,'k-')
        ax[idx_i][idx_j].loglog(Idvec/md,max_ratio,'k-')
        ax[idx_i][idx_j].fill_between(Idvec/md,min_ratio,max_ratio,color=(0.5,0.5,0.5,0.5))
        
        try:
            ax[idx_i][idx_j].plot(xp_data[:,0],xp_data[:,1],'ko')
        except:
            ax[idx_i][idx_j].plot(xp_data[idx][:,0],xp_data[idx][:,1],'ko')
    
    # Plot labels and limits
    ax[idx_i][idx_j].set_xlabel("Id / mdot")
    ax[idx_i][idx_j].set_ylabel("P / Pmag")
    ax[idx_i][idx_j].set_xlim(lims[0,:])
    ax[idx_i][idx_j].set_ylim(lims[1,:])

    idx_j = idx_j + 1
    if idx_j >= 2:
        idx_j = 0
        idx_i = idx_i + 1

plt.show()
