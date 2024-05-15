# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 09:19:05 2018

@author: Silvia
"""

import numpy as np
from FEpy import*
from Script_remeshing import*
from numpy import array
from scipy.interpolate import griddata
from scipy.interpolate import LinearNDInterpolator

filename = 'apply_displacements3.inp'
write_poly2(filename)