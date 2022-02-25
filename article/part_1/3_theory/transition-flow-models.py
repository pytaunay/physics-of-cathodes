# MIT License
# 
# Copyright (c) 2022- Pierre-Yves Taunay 
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
'''
File: transition-flow-models.py
Date: February, 2022
Author: Pierre-Yves Taunay

Description: compares the ratio the total capacitance to the aperture capacitance as computed with
the approximation from [1] to both experimental [2] and numerical [3] results. 
Reproduces Figure 11 in Part 1 of the associated journal article. 

References:
    - [1] Santeler, D. J., “Exit loss in viscous tube flow,” Journal of Vacuum Science & Technology
      A: Vacuum, Surfaces, and Films, Vol. 4, No. 3, 1986, pp. 348–352 
    - [2] Jitschin, W., Ronzheimer, M., and Khodabakhshi, S., “Gas flow measurement by means of
      orifices and Venturi tubes,” Vacuum, Vol. 53, No. 1-2, 1999, pp. 181–185. 
    - [3] Sharipov, F., “Numerical simulation of rarefied gas flow through a thin orifice,” Journal
      of Fluid Mechanics, Vol. 518, 2004, pp. 35. 

'''
import matplotlib.pyplot as plt
import numpy as np

import cathode.constants as cc
import cathode.models.flow as cmf

# Knudsen numbers, constants
Knvec = np.logspace(-4,1,100)
gam = 5./3.

# Values that cancel out
Teq = 1 
ro = 1
M = 1

# Theta
th = cmf.santeler_theta(Knvec) 

### Compute conductances
# Molecular conductance, Cm
Ca = np.pi * ro**2 * np.sqrt(cc.Boltzmann * Teq / (2 * np.pi * M)) # Aperture conductance (n * cbar / 4)
Cm = Ca # Molecular flow conductance

# Viscous flow conductance, Cv
exponent = (gam+1)/(gam-1)
Ca_v = np.pi * ro**2 * np.sqrt(cc.Boltzmann * Teq / (2 * np.pi * M))
Ggam = np.sqrt(gam * (2/(gam+1))**exponent)
Cz = np.sqrt(2*np.pi) * Ca_v
Cv = Ggam * Cz 

# Total conductance from model
Ct = (th * Cm + (1-th)*Cv)

### Experimental and numerical data
xp_data = np.array([
[10.1690410387301,1.00295],
[3.05372553054125,1.01844],
[0.988097953941127,1.05566],
[0.484942224162422,1.12564],
[0.182444174179741,1.28033],
[0.0870041563164429,1.40267],
[0.0373860859435039,1.51591],
[0.0188973105443168,1.57327],
[0.00997975776627239,1.59092],
[0.00511564030007004,1.60315],
[0.00232755525655428,1.59543],
[0.000940156168803569,1.5768],
[0.000447239342157525,1.56731],
[0.000215928515991667,1.55421],
[0.000112302648860286,1.54838],
])

num_data = np.array([
[3.42496639016581,1.01742],
[1.36397469765389,1.03567],
[0.903766655613985,1.05469],
[0.545501958342267,1.08588],
[0.342323184869325,1.13],
[0.271816811679347,1.15663],
[0.179964280336848,1.21292],
[0.13602424186644,1.25705],
[0.0895955240520534,1.32703],
[0.0670527067675249,1.37496],
[0.0542920592076485,1.40539],
[0.0448318142317753,1.43126],
[0.0337276679859221,1.46397],
[0.0267852876110755,1.48299],
[0.0178322569766117,1.50961],
[0.013421353463044,1.52102],
[0.00885148859342976,1.52863],
[0.00531932240816927,1.53548],
[0.00335750226281153,1.53472],
[0.00265458303178488,1.53243],
[0.00133775417191216,1.53015],
])


### Plot
plt.semilogx(Knvec,Ct/Ca,'k-')
plt.plot(xp_data[:,0], xp_data[:,1], 'ko')
plt.plot(num_data[:,0], num_data[:,1], 'k^')

plt.xlabel("Knudsen number")
plt.ylabel("Total conductance / Aperture conductance")

plt.show()
