import numpy as np  
from odbAccess import *
import os
import sys

it = 3
name = 'resultsFolder\\it_%i\\applyReac2\\apply_reactions_2_new.odb' % (int(it))

odb = openOdb(name)
StepName = 'Reactions_imposed'
Variable = 'LE'
PartName = 'PART-1-1'
nodeSetName= 'NODOS_SURFACE_CYTO'
Steps=odb.steps[StepName]
stepFrame=Steps.frames[-1]

nodeSetName = 'NODOS_SURFACE_CYTO'
nodes = odb.rootAssembly.instances[PartName].nodeSets[nodeSetName].nodes
nodes_surface = np.zeros((len(nodes)))
for i in range (0, len(nodes)):
	nodes_surface[i] = nodes[i].label


ElemSetName = 'ELEMENT_CYTO'
elem = odb.rootAssembly.instances[PartName].elementSets[ElemSetName].elements
conect = np.zeros((len(elem),1))
for i in range (0, len(elem)):
	conect[i,0] = odb.rootAssembly.instances[PartName].elementSets[ElemSetName].elements[i].label

NameOfFile = 'LE_todosElems%i.txt' % (int(it))
FileResults = open(NameOfFile,'w')
FileResults = open(NameOfFile,'w')
for i in range (0, len(elem)):
	data = stepFrame.fieldOutputs[Variable].values[conect[i].astype(int)-1]
	FileResults.write('%1.0f\t %s\n' %(conect[i], ' '.join(format(x, "10.7E") for x in data.data)))
FileResults.close()