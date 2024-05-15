# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 09:15:09 2018

@author: Silvia
"""

import numpy as np
from FEpy import*
from Script_remeshing import*
from numpy import array
from scipy.interpolate import griddata
from scipy.interpolate import LinearNDInterpolator

with open('apply_displacements.inp','r') as file:
    filedata=file.read()
    filedata=filedata.replace(",\n*Nset, nset=", "\n*Nset, nset=")
    filedata=filedata.replace(",\n*Elset, elset=", "\n*Elset, elset=")
with open('apply_displacements.inp','w') as file:
        file.write(filedata)
filename = 'apply_displacements.inp'
# Import the voxel mesh and delete the cell part in order to mesh the surface in quad elements
delete_cell2(filename)
