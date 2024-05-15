import numpy as np  #NumPy is a general-purpose array-processing package
                    #designed to efficiently manipulate large
                    #multi-dimensional arrays

from odbAccess import *
# module to have access to odb output files of Abaqus simulations

import os

import sys
#This module provides a number of functions and variables that can
#be used to manipulate different parts of the Python runtime environment

def get_inc():
    f = open('apply_reactions_new.sta', 'r')
    lines = f.readlines()
    line = lines[-3]
    array = np.fromstring(line, dtype=int, sep='     ')
    inc = array[-1]
    print ('ok')
    return inc

name='apply_displacements_new.odb'; # sys.argv, contains the command-line arguments passed to the script

StepName = 'Displacements_imposed'         #Name of the step of interest

Variable = 'RF'             #Name of the Variable 1

#inc = sys.argv[-1];
inc = get_inc()

PartName = 'PART-1-1'       #Name of the Part
nodeSetName= 'NODOS_SURFACE_CYTO'		# If the node set is 'all nodes', we do not need to call the nodes 
							# in the instance PartName
							


odb = openOdb(name)
Steps=odb.steps[StepName]

stepFrame=Steps.frames[inc-1] # last step minus one

#subset=odb.rootAssembly.instances[PartName].nodeSets[nodeSetName].nodes[0]
subset=odb.rootAssembly.instances[PartName].nodes[0]

Field=stepFrame.fieldOutputs[Variable].getSubset(position = NODAL)

fieldValues=Field.values

# directory='PRUEBA_TEMP'
# if not os.path.exists(directory):
    # os.mkdir(directory)
# os.chdir(directory)

NameOfFile = 'reactions_input2.txt'
FileResults = open(NameOfFile,'w')
# FileResults.write('Nodo \t temperatura \n')

for val in fieldValues:
	FileResults.write('%1.0f\t %10.7E\t %10.7E\t %10.7E\n' %(val.nodeLabel , val.data[0], val.data[1], val.data[2]))

FileResults.close()
