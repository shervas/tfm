import numpy as np  #NumPy is a general-purpose array-processing package
                    #designed to efficiently manipulate large
                    #multi-dimensional arrays

from odbAccess import *
# module to have access to odb output files of Abaqus simulations

import os

import sys
#This module provides a number of functions and variables that can
#be used to manipulate different parts of the Python runtime environment


name = 'apply_reactions_new.odb'

StepName = 'Reactions_imposed'         #Name of the step of interest

Variable = 'U'             #Name of the Variable 1


PartName = 'PART-1-1'       #Name of the Part

odb = openOdb(name)
Steps=odb.steps[StepName]

stepFrame=Steps.frames[-1]


nodes_gel = np.zeros(len(odb.rootAssembly.instances[PartName].nodeSets['NODOS_SOLO_GEL'].nodes))
for i in range (0,len(nodes_gel)):
    nodes_gel[i] = odb.rootAssembly.instances[PartName].nodeSets['NODOS_SOLO_GEL'].nodes[i].label

nodes_surface = np.zeros(len(odb.rootAssembly.instances[PartName].nodeSets['NODOS_SURFACE_GEL'].nodes))
for i in range (0,len(nodes_surface)):
    nodes_surface[i] = odb.rootAssembly.instances[PartName].nodeSets['NODOS_SURFACE_GEL'].nodes[i].label

nodes_t = np.setdiff1d(nodes_gel, nodes_surface)

NameOfFile = 'displac_output.txt'
FileResults = open(NameOfFile,'w')
nodes = odb.rootAssembly.instances[PartName].nodeSets[nodeSetName].nodes
for i in range (0, len(nodes_t)-1):
	data = stepFrame.fieldOutputs[Variable].values[int(nodes_t[i])-1]
	FileResults.write('%1.0f\t %10.7E\t %10.7E\t %10.7E\n' %(nodes_t[i] , data.data[0], data.data[1], data.data[2]))
FileResults.close()

