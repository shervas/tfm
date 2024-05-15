import shutil
import fileinput
import re

l = []

infile = open('reactions_output.txt', 'r')

for line in infile:
    li = line.strip()
    if not li.startswith("#"):

        l.append(li.rstrip().split( ))

infile.close()

r = len(l)
print('The number of nodes to apply reactions are:')
print(r)

nodes = [row[0] for row in l]
reac_x = [row[1] for row in l]
reac_y = [row[2] for row in l]
reac_z = [row[3] for row in l]


print('Text to search for:')
textToSearch1 = 'model=NO'
textToSearch2 = '** STEP: Displacements_imposed'
print(textToSearch2)


print('Text to replace it with:')
textToReplace1 = 'model=YES'
textToReplace2 = """** STEP: Reactions_imposed
**
*Step, name=Reactions_imposed, NLGEOM=YES
*Static
0.05, 1., 1e-05, 1.
** LOADS
**
*Cload
"""
print(textToReplace2)


shutil.copy2('./apply_displacements4.inp', './apply_reactions_2_new.inp')


print("File to perform Search-Replace on displacements field:")
fileToSearch = './apply_reactions_2_new.inp'
print(fileToSearch)


for line in fileinput.input(fileToSearch, inplace=True):
    print (line.replace(textToSearch1, textToReplace1).replace(textToSearch2, textToReplace2), end='')


outfile = open('apply_reactions_2_new.inp', 'a')

for index in range(len(nodes)):
    outfile.write(str(nodes[index]) + ", 1, " + str(float(reac_x[index])*(1)) + "\n")
    outfile.write(str(nodes[index]) + ", 2, " + str(float(reac_y[index])*(1)) + "\n")
    outfile.write(str(nodes[index]) + ", 3, " + str(float(reac_z[index])*(1)) + "\n")

outfile.write("""***********************************************************
** OUTPUT REQUESTS
**
*RESTART, WRITE, FREQUENCY=0
*OUTPUT,FIELD, frequency=99999
*NODE OUTPUT
CF, U
*Output, field, frequency=99999
*Element Output, directions=YES
LE, NE
*END STEP
""")
outfile.close()

print('New input file completed')
print('\n\n Press Enter to exit...')
