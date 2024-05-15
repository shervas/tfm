##########################################################################################################
# This file is part of the method that will be soon published in
#
#
# If you use any part of it, please cite this paper.
###########################################################################################################
import shutil
import tempfile
import fileinput
import re
l = []

infile = open('displacements_input2.txt', 'r')

for line in infile:
    li = line.strip()
    if not li.startswith("#"):

        l.append(li.rstrip().split( ))

infile.close()

r = len(l)
print('The number of nodes to apply displacements are:')
print(r)

nodes = [row[0] for row in l]
disp_x = [row[1] for row in l]
disp_y = [row[2] for row in l]
disp_z = [row[3] for row in l]

print('Text to search for:')
textToSearch1 = 'model=NO'
textToSearch2 = '** STEP: Displacements_imposed'

print(textToSearch2)


print("Text to replace it with:")
textToReplace1 = 'model=YES'
textToReplace2 = """** STEP: Displacements_imposed
**
*Step, name=Displacements_imposed, NLGEOM=YES
*Static
0.005, 1., 1.2e-06, 0.1
**
** BOUNDARY CONDITIONS
**
*Boundary"""
print(textToReplace2)

###############################################################


shutil.copy2('./apply_displacements4.inp', './apply_displacements_new.inp')


print('File to perform Search-Replace on displacements field:')
fileToSearch = './apply_displacements_new.inp'
print(fileToSearch)


for line in fileinput.input(fileToSearch, inplace=True):
    print(line.replace(textToSearch1, textToReplace1).replace(textToSearch2, textToReplace2), end='')

###############################################################

outfile = open('apply_displacements_new.inp', 'a')

for index in range(len(nodes)):
    outfile.write(str(nodes[index]) + ", 1, 1, " + str(float(disp_x[index])*(-1)) + "\n")
    outfile.write(str(nodes[index]) + ", 2, 2, " + str(float(disp_y[index])*(-1)) + "\n")
    outfile.write(str(nodes[index]) + ", 3, 3, " + str(float(disp_z[index])*(-1)) + "\n")

outfile.write("""NODOS_SURFACE_CYTO, 1, 3, 0
***********************************************************
** OUTPUT REQUESTS
**
*RESTART, WRITE, FREQUENCY=0
*OUTPUT, FIELD, frequency=99999
*NODE OUTPUT
RF, U
*Output, field, frequency=99999
***Element Output, directions=YES
**LE, NE, S
*END STEP
""")
outfile.close()

print('New input file completed')
print('\n\n Press Enter to exit...' )
