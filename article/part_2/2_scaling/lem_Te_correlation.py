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
File: lem_Te_correlation.py
Author: Pierre-Yves Taunay
Date: February, 2022
Description: generate Fig. 5 in Part 2 of Physics of Thermionic Orificed Hollow Cathodes.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cathode.constants as cc

### Path to HDF5 file
hdf5_paths = [
        '../../../results/nstar.h5',
        '../../../results/nstar.h5',
        '../../../results/nexis.h5',
        '../../../results/nexis.h5',
        '../../../results/nexis_do-2.0mm.h5',
        '../../../results/nexis_do-2.0mm.h5',
        '../../../results/jpl_lab6.h5',
        '../../../results/jpl_lab6.h5',
        #'../../../results/jpl_lab6_2cm_do-3.8mm.h5',
        '../../../results/jpl_lab6_2cm_do-6.4mm.h5',
        '../../../results/salhi_xe.h5',
        '../../../results/siegfried.h5',
        ]
key_root = 'Xe/simulations/results/'

end_keys = [
        ['r20210304185153','r20210304185359','r20210304185623'], # NSTAR, 2.47 sccm, 8.29 A
        ['r20210304185851','r20210304190116','r20210304190330'], # NSTAR 3.7 sccm, 13.2 A
        ['r20210305163012','r20210305164507','r20210305170023'], # NEXIS 5.5 sccm, 25 A, 2.75 mm 
        ['r20210304192828','r20210304193119','r20210304193415'], # NEXIS 10.0 sccm, 25 A, 2.75 mm 
        ['r20210304211359','r20210304211620','r20210304211840'], # NEXIS 2.0 mm 
        ['r20210304211359','r20210304211620','r20210304211840'], # NEXIS 2.0 mm 
        ['r20210303211954','r20210303213415','r20210303214842'], # JPL 1.5 cm
        ['r20210303211954','r20210303213415','r20210303214842'], # JPL 1.5 cm
        #['r20210609165949','r20210609170939','r20210609171930'], # JPL 2.0 cm
        ['r20210609202654','r20210609203634','r20210609204616'], # JPL 2.0 cm
        ['r20210304172101','r20210304172637','r20210304173212'], # Salhi Xe
        ['r20210305021601','r20210305022632','r20210305023703'], # Siegfried and Wilbur
        ]

Tgvec = [2000,3000,4000]

# mass flow rate (sccm), discharge current, Lem, Lem error
xp_lem_all = [
        # NSTAR
        np.array([
            [2.47, 8.29, 0.53050250916374087,0.061494936172353541], 
            ]),
        np.array([
            [3.7, 13.2, 0.437095767283502, 0.0596160278227]
            ]),
        # NEXIS 2.75 mm orifice
        np.array([
            [5.5, 25.0, 0.502924752280311,0.104167073653],
            ]),
        np.array([
            [10.0, 25.0, 0.460793,0.085712]
            ]),
        # NEXIS 2.0 mm orifice
        np.array([
            [5.5, 25.0, 0.34930177041878169,0.096754214171287073],
            ]),
        np.array([
            [10.0, 25.0, 0.33832219159751992,0.060160460906435065]
            ]),
        # JPL 1.5 cm cathode
        np.array([
            [8.0,20.0,0.58720030212,0.116664079989],
            [8.0,30.0,0.533589413381,0.132413703393],
            [8.0,40.0,0.67429445503,0.152640573619],
            [8.0,50.0,0.60740023117,0.132866138551],
            [8.0,60.0,0.62992468652,0.13449416021],
            [8.0,70.0,0.573557995218,0.124295484781],
            [8.0,80.0,0.573657258458,0.117647574019],
            [8.0,90.0,0.477010349112,0.151869201954],
            [8.0,100.0,0.428181145236,0.0710545228643]
            ]),
        np.array([
            [12.0,20.0,0.436996003135,0.0501554027827],
            [12.0,30.0,0.407687660772,0.0698057014419],
            [12.0,40.0,0.408506452306,0.0896716963446],
            [12.0,50.0,0.421746067047,0.113291160418],
            [12.0,60.0,0.364722366088,0.166748276153],
            [12.0,70.0,0.372709013714,0.0847913232138],
            [12.0,80.0,0.430226686184,0.0626863105143],
            [12.0,90.0,0.407620207491,0.0551688232317],
            [12.0,100.0,0.428089621117,0.0620896520614],
            ]),
        # JPL 2.0 cm cathode
        np.array([
            [16.0,40.0, 0.441709,0.150931],
            [16.0,68.8,0.384544,0.085342],
            [16.0,80.0,0.313184,0.055010],
            [16.0,125.0,0.344715,0.059719],
            [16.0,150.0,0.386891,0.058663],
            [16.0,200.0,0.293621,0.054599]
            ]),
        # Salhi Xe
        np.array(
            [
            [0.5/cc.sccm2eqA,5.0,0.344380,0.081339],
            [0.5/cc.sccm2eqA,9.0,0.31421574796719,0.0742309185405],
            [0.5/cc.sccm2eqA,12.0,0.282429429616658,0.06680724419527],
            [0.5/cc.sccm2eqA,15.0,0.439504506861141,0.127464586651]
            ]),
        # Siegfried and Wilbur
        np.array([
            [1.77, 2.3, 0.399498,0.093400]
            ])
        ]

xp_te_all = [
        # NSTAR
        np.array([
            [2.47, 8.29,1.427740,0.5], 
            ]),
        np.array([
            [3.7, 13.2,1.38071637828435,0.5]
            ]),
        # NEXIS 2.75 mm orifice
        np.array([
            [5.5, 10.0,3.76, 0.5 ],
            [5.5, 25.0,2.11151774806103, 0.5]
            ]),
        np.array([
            [10.0, 25.0, 1.754809,0.5]
            ]),
        # NEXIS 2.0 mm orifice
        np.array([
            [0.0, 25.0, 0.34930177041878169,0.096754214171287073],
            ]),
        np.array([
            [0.0, 25.0, 0.33832219159751992,0.060160460906435065]
            ]),
        # JPL 1.5 cm cathode
        np.array([
            [8.0,20,2.26648,0.5],
            [8.0,30,2.25549,0.5],
            [8.0,40,2.2033,0.5],
            [8.0,50,1.7838716696245,0.5],
            [8.0,60,2.1978,0.5],
            [8.0,70,2.17033,0.5],
            [8.0,80,2.09615,0.5],
            [8.0,100,1.98345050689552,0.5],
            [8.0,90,2.13736,0.5],
            ]),
        np.array([
            [12.0,20,1.73626,0.5],
            [12.0,30,1.79121,0.5],
            [12.0,40,1.68132,0.5],
            [12.0,50,1.5476210306236,0.5],
            [12.0,90,1.57418,0.5],
            [12.0,60,1.45055,0.5],
            [12.0,70,1.6978,0.5],
            [12.0,80,1.60989,0.5],
            [12.0,100,1.69163582541647,0.5],
            ]),
        # JPL 2.0 cm cathode
        np.array([
            [1.0,40.0, 0.441709,0.150931],
            [1.0,68.8,0.384544,0.085342],
            [1.0,80.0,0.313184,0.055010],
            [1.0,125.0,0.344715,0.059719],
            [1.0,150.0,0.386891,0.058663],
            [1.0,200.0,0.293621,0.054599]
            ]),
        # Salhi Xe
        np.array(
            [
[0.5/cc.sccm2eqA,5.0,1.113016,0.5],
[0.5/cc.sccm2eqA,9.0,1.085291,0.5],
[0.5/cc.sccm2eqA,10.0,0.98,0.12],
[0.5/cc.sccm2eqA,15.0,0.966499173349343,0.5],
[0.5/cc.sccm2eqA,20.0,1.07,0.15],
]),
        # Siegfried and Wilbur
        np.array([
            [1.943,2.3,1.0697,0.5],
            [2.444,2.3,0.799212,0.5],
            [3.4856,2.3,0.878997,0.5],
            [4.0238,2.3,0.709722,0.5],
            [5.357,2.3,0.647433,0.5],
            [6.39755,2.3,0.763997,0.5],
            [7.3448,2.3,0.609152,0.5],
            ])
        ]

        

fig, ax = plt.subplots(2,1)
for path_to_results, key_end, lem_data, te_data in zip(hdf5_paths,end_keys,xp_lem_all, xp_te_all):
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

    ### Find the minimum and maximum bounds for each data point
    # Here we have as many discharge current points as there are data points
    dc = np.unique(dfall['insertDiameter'])
    
    ### Attachment length
    # Plot the bounds and fill the area for each mass flow rate
    mdvec = np.unique(lem_data[:,0])
    Idvec = (lem_data[:,1])

    min_pd = np.zeros_like(Idvec)
    max_pd = np.zeros_like(Idvec)
    ave_pd = np.zeros_like(Idvec)
    xerr = np.zeros((2,len(ave_pd)))

    for idx, md in enumerate(mdvec):
        dfx = dfall[np.isclose(dfall['massFlowRate_sccm'],md)]
        
        xp_lem = np.copy(lem_data)

        if not dfx.empty:
            # Populate vectors to plot
            for kk, Id in enumerate(Idvec):
                dfxx = dfx[dfx['dischargeCurrent'] == Id]

                if not dfxx.empty:
                    min_pd[kk] = np.nanmin(dfxx['neutralPressure'] / cc.Torr * dfxx['insertDiameter'] * 1e2)
                    max_pd[kk] = np.nanmax(dfxx['neutralPressure'] / cc.Torr * dfxx['insertDiameter'] * 1e2)
                    ave_pd[kk] = np.nanmean(dfxx['neutralPressure'] / cc.Torr * dfxx['insertDiameter'] * 1e2)
            
            xerr[0,:] = np.copy(ave_pd-min_pd)
            xerr[1,:] = np.copy(max_pd-ave_pd)

            fmt = 'ko'

            ax[0].errorbar(ave_pd, xp_lem[:,2], yerr=xp_lem[:,3], xerr=xerr, fmt=fmt)


    ### Electron temperature 
    # Plot the bounds and fill the area for each mass flow rate
    mdvec = np.unique(te_data[:,0])
    Idvec = (te_data[:,1])

    min_pd = np.zeros_like(Idvec)
    max_pd = np.zeros_like(Idvec)
    ave_pd = np.zeros_like(Idvec)
    xerr = np.zeros((2,len(ave_pd)))

    for idx, md in enumerate(mdvec):
        dfx = dfall[np.isclose(dfall['massFlowRate_sccm'],md,1e-4)]
        
        xp_te = np.copy(te_data)

        if not dfx.empty:

            # Populate vectors to plot
            for kk, Id in enumerate(Idvec):
                dfxx = dfx[dfx['dischargeCurrent'] == Id]

                if not dfxx.empty:
                    min_pd[kk] = np.nanmin(dfxx['neutralPressure'] / cc.Torr * dfxx['insertDiameter'] * 1e2)
                    max_pd[kk] = np.nanmax(dfxx['neutralPressure'] / cc.Torr * dfxx['insertDiameter'] * 1e2)
                    ave_pd[kk] = np.nanmean(dfxx['neutralPressure'] / cc.Torr * dfxx['insertDiameter'] * 1e2)
            
            xerr[0,:] = np.copy(ave_pd-min_pd)
            xerr[1,:] = np.copy(max_pd-ave_pd)

            # Trick for S&W to avoid plotting the same data multiple times
            if Id == 2.3:
                print(ave_pd[idx],xp_te[idx,2],xerr[0,idx])
                ax[1].errorbar(ave_pd[idx], xp_te[idx,2], yerr=xp_te[idx,3],
                        xerr=np.array([
                            [xerr[0,idx]],
                            [xerr[1,idx]]]),fmt='ko')
            else:
                ax[1].errorbar(ave_pd, xp_te[:,2], yerr=xp_te[:,3], xerr=xerr, fmt='ko')

            print(path_to_results, md*cc.sccm2eqA, ave_pd, xp_te[:,2])

    
### Plot correlation from diffusion theory
pdvec = np.logspace(-1,1,100)
lem_theory = 0.5*(0.72389 + 0.17565 / pdvec**1.22140) 
te_theory = 0.52523 + 1.20072 / pdvec**0.35592
ax[0].semilogx(pdvec,lem_theory,'k-')
ax[1].semilogx(pdvec,te_theory,'k-')


#### Labels
ax[0].set_xlabel('Neutral pressure - diameter product (Torr-cm)')
ax[0].set_ylabel('Emission length / insert diameter')
ax[0].set_xlim([0.1,10])
ax[0].set_ylim([0,1])
ax[0].set_xscale('log')

ax[0].set_xlabel('Neutral pressure - diameter product (Torr-cm)')
ax[1].set_ylabel('Insert electron temperature (eV)')
ax[1].set_xlim([0.1,10])
ax[1].set_ylim([0,3])
ax[1].set_xscale('log')

plt.show()
