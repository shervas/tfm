import shutil
import numpy as np
import fileinput
from scipy import stats

l = []

infile = open('reactions_input.txt', 'r')

for line in infile:
    li=line.strip()
    if not li.startswith("#"):
        l.append(li.rstrip().split())

infile.close()


r = len(l)
print('The number of nodes to apply reactions are:')
print(r)


print("Text to search for:")
textToSearch1 = 'model=NO'
textToSearch2 = '** STEP: Displacements_imposed'
print(textToSearch2)


print("Text to replace it with:")
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

shutil.copy2('./apply_displacements4.inp', './apply_reactions_new.inp')


print('File to perform Search-Replace on displacements field:')
fileToSearch = './apply_reactions_new.inp'
print(fileToSearch)


for line in fileinput.input(fileToSearch, inplace=True):
    print(line.replace(textToSearch1, textToReplace1).replace(textToSearch2, textToReplace2), end='')


for n in range(0, r):
    l[n][1] = round(1 * float( l[n][1] ), 4)
    l[n][2] = round(1 * float( l[n][2] ), 4)
    l[n][3] = round(1 * float( l[n][3] ), 4)

nodes = [row[0] for row in l]
reac_x = [row[1] for row in l]
reac_y = [row[2] for row in l]
reac_z = [row[3] for row in l]


outfile = open('apply_reactions_new.inp', 'a')

data = np.genfromtxt('reactions_input.txt')

#Calculate the magnitude of the forces
data = np.append(data, np.ones((len(data),1)), axis=1)
data[:,4] = [np.sqrt((float(x)**2 + float(y)**2 + float(z)**2)) for x, y, z in zip(data[:,1], data[:,2], data[:,3])]

zeros = np.zeros((len(data)))
zeros[:] = data[:,4].astype(int) == 0 
data_rm = np.zeros((len(np.argwhere(zeros[:] == 0)),5))
cont = 0
for i in range (0, len(data)):
    if zeros[i] == 0:
        data_rm[cont,:] = data[i,:]
        cont +=1  
data_rm = data_rm[~(data_rm==0).all(1)]

#Sort the reactions in absolute value, extract the intervals and filter out
reac_ms = sorted(np.absolute(data_rm[:,4]))
q1x, q3x = np.percentile(reac_ms,[25,75])
iqrx = q3x-q1x
reac_m_pre = [x if (q1x - (40*iqrx) <= x <= q3x + (40*iqrx)) else (0 if (x < q1x - (40*iqrx)) else 0) for x in data_rm[:,4]]

min_reacms = 0
max_reacms = 0
reac_m = [x if (q1x - (40*iqrx) <= x <= q3x + (40*iqrx)) else (min_reacms if (x < q1x - (40*iqrx)) else max_reacms) for x in data_rm[:,4]]

#Transform from magnitude to coordinates
data2 = np.zeros((np.shape(data_rm)))
data2[:,0] = data_rm[:,0]
data2[:,1] = [float(x)*float(y)/float(z) for x, y, z in zip(reac_m[:], data_rm[:,1], data_rm[:,4])]
data2[:,2] = [float(x)*float(y)/float(z) for x, y, z in zip(reac_m[:], data_rm[:,2], data_rm[:,4])]
data2[:,3] = [float(x)*float(y)/float(z) for x, y, z in zip(reac_m[:], data_rm[:,3], data_rm[:,4])]
data2[:,4] = reac_m[:]


for index in range(len(data2)):
    outfile.write(str(int(data2[index,0])) + ", 1, " + str(float(data2[index,1])*(-1)) + "\n")
    outfile.write(str(int(data2[index,0])) + ", 2, " + str(float(data2[index,2])*(-1)) + "\n")
    outfile.write(str(int(data2[index,0])) + ", 3, " + str(float(data2[index,3])*(-1)) + "\n")
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

newreactfile = open('reactions_input_new.txt', 'w')
for index in range(len(data2)):
     newreactfile.write(str(int(data2[index,0])) + "     " + str(float(data2[index,1])) + "     " + str(float(data2[index,2]))+ "     " + str(float(data2[index,3])) + "\n")     
newreactfile.close()

print('New input file completed')
print('\n\n Press Enter to exit...')
