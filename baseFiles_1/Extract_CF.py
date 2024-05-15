import numpy as np  #NumPy is a general-purpose array-processing package
                    #designed to efficiently manipulate large
                    #multi-dimensional arrays

from odbAccess import *
# module to have access to odb output files of Abaqus simulations

import os

import sys
#This module provides a number of functions and variables that can
#be used to manipulate different parts of the Python runtime environment

name='applyReac/apply_reactions_new.odb'; # sys.argv, contains the command-line arguments passed to the script

StepName = 'Reactions_imposed'         #Name of the step of interest

Variable = 'CF'             #Name of the Variable 1

PartName = 'PART-1-1'       #Name of the Part
nodeSetName= 'NODOS_SURFACE_CYTO'        # If the node set is 'all nodes', we do not need to call the nodes 
                            # in the instance PartName
                            
odb = openOdb(name)
Steps=odb.steps[StepName]
stepFrame=Steps.frames[-1]
subset=odb.rootAssembly.instances[PartName].nodeSets[nodeSetName].nodes
Field=stepFrame.fieldOutputs[Variable].getSubset(position = NODAL)
fieldValues=Field.values

NameOfFile = 'reactions_input2.txt'
FileResults = open(NameOfFile,'w')

for i in range (0,len(subset)):
	data = fieldValues[subset[i].label-1].data
	FileResults.write('%1.0f\t %10.7E\t %10.7E\t %10.7E\n' %(fieldValues[subset[i].label-1].nodeLabel,data[0],data[1],data[2]))

FileResults.close()