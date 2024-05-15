# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior

a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
mdb.ModelFromInputFile(name='apply_displacements2', 
	inputFileName='apply_displacements2.inp')
a = mdb.models['apply_displacements2'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
	meshTechnique=ON)
p = mdb.models['apply_displacements2'].parts['PART-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
	meshTechnique=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
	referenceRepresentation=OFF)
p = mdb.models['apply_displacements2'].parts['PART-1']
p.convertSolidMeshToShell()
mdb.meshEditOptions.setValues(enableUndo=True, maxUndoCacheElements=0.5)
p = mdb.models['apply_displacements2'].parts['PART-1']
p.renumberNode(startLabel=1, increment=1)
a = mdb.models['apply_displacements2'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
	meshTechnique=OFF)
a2 = mdb.models['apply_displacements2'].rootAssembly
p = mdb.models['apply_displacements2'].parts['PART-1']
a2.Instance(name='PART-1-1', part=p, dependent=ON)	
mdb.Job(name='apply_displacements3', model='apply_displacements2', 
	description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, 
	queue=None, memory=90, memoryUnits=PERCENTAGE, 
	getMemoryFromAnalysis=True, explicitPrecision=SINGLE, 
	nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
	contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
	resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=1, 
	activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)
mdb.jobs['apply_displacements3'].writeInput(consistencyChecking=OFF)
