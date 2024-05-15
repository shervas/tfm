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
import os
import numpy as np
session.openOdb("apply_reactions_2_new.odb")
odb = session.odbs['apply_reactions_2_new.odb']
p = mdb.models['Model-1'].PartFromOdb(name='PART-1-1', instance='PART-1-1', 
	odb=odb, shape=DEFORMED, step=0, frame=-1)
p = mdb.models['Model-1'].parts['PART-1-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
odb.close()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
	optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['PART-1-1']
a.Instance(name='PART-1-1-1', part=p, dependent=ON)

jobName = 'apply_displacements'
myJob = mdb.Job(name=jobName, model='Model-1')
myJob.writeInput()

infile = open('apply_displacements.inp', 'r')
filedata = infile.read()
a = (', generate' in filedata)
infile.close()

infile = open('apply_displacements.inp', 'r')
cont=0
cont_gen=0
l = []
generate = np.zeros(20)
if (a==True):
    for line in infile:
        cont=cont+1
        li=line.strip()
        if 'generate' in li:
            generate[cont_gen] = cont
            cont_gen = cont_gen+1
        if not li.startswith("#"):
            l.append(li.rstrip().split())
    generate = generate[~(generate==0)]
    infile.close()
    outfile = open('apply_displacements.inp', 'w')
    for i,line in enumerate(l,0):
        if i not in generate:
            outfile.writelines(" ".join(line))
            outfile.write('\n')
        else:
            k = np.argwhere(i==generate)
            start = int(l[int(generate[k])][0].strip(', '))
            stop = int(l[int(generate[k])][1].strip(', '))
            step = int(l[int(generate[k])][2].strip(', '))
            nodes = np.linspace(start,stop,num=int(1+(stop-start)/step))
            count = 0
            nodes_str = ''
            for i in range(0, len(nodes)):
                nodes_str += ' %i, ' % (nodes[i])
                count += 1
                if count == 16:
                    nodes_str = nodes_str[:-2] + '\n'
                    count = 0 
                elif i == (len(nodes) - 1):
                    nodes_str = nodes_str[:-2]
                else:
                    pass
            if nodes_str[-1] == '\n':
                nodes_str = nodes_str[:-1]
            outfile.write(nodes_str)
            outfile.write('\n')
    outfile.close()
    
    with open('apply_displacements.inp','r') as file:
        filedata=file.read()
        filedata=filedata.replace(', generate\n','\n')
    with open('apply_displacements.inp','w') as file:
        file.write(filedata)
else:
    pass