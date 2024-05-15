# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 09:23:56 2018

@author: Silvia
"""

import numpy as np
from FEpy import*
from Script_remeshing import*
from numpy import array
from scipy.interpolate import griddata
from scipy.interpolate import LinearNDInterpolator

tetgen2inp()
