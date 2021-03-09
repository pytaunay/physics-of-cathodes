import numpy as np
import h5py
import pandas as pd

import matplotlib.pyplot as plt
import scipy.optimize as root

from cathode.models.flow import poiseuille_flow, reynolds_number
from cathode.models.taunay_et_al import solve
import cathode.constants as cc


cat = 'PLHC'

do_db = 0.22 * 25.4
dc_db = 27.15
M_db = 39.948
Lo_db = 1.5
eiz_db = 15.7596

# Transform database results
M = M_db * cc.atomic_mass
dc = dc_db * 1e-3
do = do_db * 1e-3
Lo = Lo_db * 1e-3
species = 'Ar'

Lupstream = (8+3/4) * 2.54e-2
Lemitter = 8e-2

phisvec = np.array([1],dtype=np.float64)
mdotvec = np.array([108.75],dtype=np.float64)
Idvec = np.array([100],dtype=np.float64)

mdotvec *= cc.sccm2eqA
TgK = 3000.

path, df = solve(Idvec, mdotvec, M_db, dc_db, do_db, Lo_db, Lupstream, Lemitter, eiz_db, TgK,
                 'plhc.h5', verbose=True,phi_s=phisvec)