import shutil
import tempfile
import fileinput
import re
l = []

infile = open('displac_known2.txt', 'r')

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
0.01, 1, 1e-05, 1
**
** BOUNDARY CONDITIONS
**
*Boundary
"""
print(textToReplace2)

# ##############################################################


shutil.copy2('./apply_displacements4.inp', './apply_displacements_new.inp')


print('File to perform Search-Replace on displacements field:')
fileToSearch = './apply_displacements_new.inp'
print(fileToSearch)


for line in fileinput.input(fileToSearch, inplace=True):
    print(line.replace(textToSearch1, textToReplace1).replace(textToSearch2, textToReplace2), end='')

###############################################################

outfile = open('apply_displacements_new.inp', 'a')

for index in range(len(nodes)):
    outfile.write(str(nodes[index]) + ", 1, 1, " + str(disp_x[index]) + "\n")
    outfile.write(str(nodes[index]) + ", 2, 2, " + str(disp_y[index]) + "\n")
    outfile.write(str(nodes[index]) + ", 3, 3, " + str(disp_z[index]) + "\n")

outfile.write("""***********************************************************
** OUTPUT REQUESTS
**
*RESTART, WRITE, FREQUENCY=0
*OUTPUT, FIELD, frequency=99999
*NODE OUTPUT
RF, U
*Output, field, frequency=99999
***Element Output, directions=YES
**LE, NE, S
**NODE FILE, NSET=Nodos_Solo_Gel,FREQUENCY=99999
**U
***NODE PRINT,NSET=Nodos_Solo_Gel, FREQUENCY=99999
**U
*END STEP
""")
outfile.close()

print('New input file completed')
print('\n\n Press Enter to exit...' )
