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
plt.show()
