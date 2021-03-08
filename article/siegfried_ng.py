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
from cathode.models.taunay_et_al import solve
import cathode.constants as cc

### Name the cathode
cat = 'Siegfried-NG'
fname = 'siegfried.h5'

### Geometry in mm
do_db = 0.76    # orifice diameter
dc_db = 3.8     # insert diameter
Lo_db = 1.8     # orifice length

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
Lupstream = 1.0e-3 # Does not matter for this study
Lemitter = 2.54e-2

############################
### Run the actual cases ###
############################
# First run the orifice cases: create a grid of values
Idvec = np.array([2.2,2.4])
mdotvec = np.arange(1.5,8,0.5)
for TgK in [2000.,3000.,4000.]:
    path, df = solve(Idvec, mdotvec, M_db, dc_db, do_db, Lo_db, Lupstream, Lemitter, eiz_db, TgK,
                     fname, verbose=True,phi_s=None)

### Second run the actual cases
# Sheath voltages in V
phisvec = np.array([1,4,7,10],dtype=np.float64)

# 2.3 A, mdot = 1.9 to 7.5 sccm for electron temperature data
# 2.3 A, mdot = 1.77 sccm for emission length data
Idvec = np.array([2.3])
# We'll run all cases together
mdotvec = np.array([0.13941011, 0.17533492, 0.25007255, 0.28868797, 0.38434202, 0.45899206, 0.52695527])
mdotvec /= cc.sccm2eqA
mdotvec = np.append(mdotvec,1.77)
mdotvec = np.sort(mdotvec)
mdotvec *= cc.sccm2eqA

# Sweep over all temperatures
dflist = []
for TgK in [2000.,3000.,4000.]:
    path, df = solve(Idvec, mdotvec, M_db, dc_db, do_db, Lo_db, Lupstream, Lemitter, eiz_db, TgK,
                     fname, verbose=True,phi_s=phisvec)
    dflist.append(df)
