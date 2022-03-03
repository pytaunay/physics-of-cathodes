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

import numpy as np
import cathode.constants as cc
from cathode.models.taunay_et_al import solve

### Name the cathode
cat = 'JPL_LaB6'
fname = "jpl_lab6.h5"

### Geometry in mm
do_db = 3.8     # orifice diameter
dc_db = 7.0     # insert diameter
Lo_db = 1.0     # orifice length (assumed)

### Gas quantities: atomic mass and ionization potential
species = 'Xe'
M_db = 131.293
eiz_db = 12.1298

### Transform to SI
M = M_db * cc.atomic_mass
dc = dc_db * 1e-3
do = do_db * 1e-3
Lo = Lo_db * 1e-3

### Length of emitter and upstream pressure measurement
Lupstream = 13e-2       # Same setup as NSTAR and NEXIS
Lemitter = 2.54e-2

############################
### Run the actual cases ###
############################
phisvec = np.array([1,4,7,10],dtype=np.float64)         # Sheath voltages in V

# The 1e-5 gets around the issue of some float conversion that makes the flow rate out of bounds
# of the interpolator data
mdotvec = np.array([8.0+1e-5,12.0],dtype=np.float64)    # Mass flow rate
Idvec = np.arange(20.,110.,10.)                         # Discharge current

mdotvec *= cc.sccm2eqA

# Sweep over all temperatures
dflist = []
for TgK in [2000.,3000.,4000.]:
    path, df = solve(Idvec, mdotvec, M_db, dc_db, do_db, Lo_db, Lupstream, Lemitter, eiz_db, TgK,
                     fname, verbose=True,phi_s=phisvec)
    dflist.append(df)
