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
cat = 'Salhi-Xe'
fname = 'salhi_xe.h5'

### Geometry in mm
do_db = 1.21    # orifice diameter
dc_db = 3.81    # insert diameter
Lo_db = 1.24    # orifice length

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
Lupstream = 13e-2 # Set the same as NSTAR / NEXIS because it is not specified
Lemitter = 2.54e-2

############################
### Run the actual cases ###
############################
phisvec = np.array([1,4,7,10],dtype=np.float64)         # Sheath voltages in V

### Electron temperature and attachment length
# Id = 1,3,5,9,10,12,15,20
# mdot = 0.5 A
Idvec = np.array([1,3,5,9,10,12,15,20],dtype=np.float64)
mdotvec = np.array([0.5])

# Sweep over all temperatures
dflist = []
for TgK in [2000.,3000.,4000.]:
    path, df = solve(Idvec, mdotvec, M_db, dc_db, do_db, Lo_db, Lupstream, Lemitter, eiz_db, TgK,
                     fname, verbose=True,phi_s=phisvec)
    dflist.append(df)
