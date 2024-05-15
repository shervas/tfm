import shutil
import numpy as np
from scipy.optimize import leastsq

l = []
m = []
n = []
o = []

infile = open('displac_known2.txt', 'r')
for line in infile:
    li = line.strip()
    if not li.startswith("#"):

        l.append(li.rstrip().split( ))
infile.close()

r = len(l)
print('The number of input nodes with displacements values are:')
print(r)
#print(np.matrix(l))
# ##############################################################
outfile = open('displac_output.txt', 'r')
for line in outfile:
    li = line.strip()
    if not li.startswith("#"):
        m.append(li.rstrip().split( ))
outfile.close()

s = len(m)
print('The number of output nodes with displacements values are:')
print(s)
#print(np.matrix(m))
# ##############################################################
reacfile = open('reactions_input_new.txt', 'r')
for line in reacfile:
    li = line.strip()
    if not li.startswith("#"):
        n.append(li.rstrip().split( ))
reacfile.close()

t = len(n)
print('The number of nodes of cell contour are:')
print(t)
#print(np.matrix(n))
# ##############################################################
nodes = [row[0] for row in l]
cell_contour = [row[0] for row in n]

disp_x0 = [row[1] for row in l]
disp_y0 = [row[2] for row in l]
disp_z0 = [row[3] for row in l]
disp_x1 = [row[1] for row in m]
disp_y1 = [row[2] for row in m]
disp_z1 = [row[3] for row in m]
reac_x = [row[1] for row in n]
reac_y = [row[2] for row in n]
reac_z = [row[3] for row in n]

# #############################################################
new_reac_x = [float(x)*-1 for x in reac_x]
new_reac_y = [float(x)*-1 for x in reac_y]
new_reac_z = [float(x)*-1 for x in reac_z]

# ##########################################################################
if r == s:
    disp_x0 = [float(x)*(-1) for x in disp_x0]
    disp_x1 = [float(x) for x in disp_x1]
    disp_y0 = [float(x)*(-1) for x in disp_y0]
    disp_y1 = [float(x) for x in disp_y1]
    disp_z0 = [float(x)*(-1) for x in disp_z0]
    disp_z1 = [float(x) for x in disp_z1]

    x_new = np.array(disp_x1)
    y_new = np.array(disp_x0)
    A = np.vstack([x_new, np.ones(len(x_new))]).T
    m, c = np.linalg.lstsq(A, y_new)[0]
    print(m, c)

    x_new2 = np.array(disp_y1)
    y_new2 = np.array(disp_y0)
    B = np.vstack([x_new2, np.ones(len(x_new2))]).T
    m2, c2 = np.linalg.lstsq(B, y_new2)[0]
    print(m2, c2)

    x_new3 = np.array(disp_z1)
    y_new3 = np.array(disp_z0)
    C = np.vstack([x_new3, np.ones(len(x_new3))]).T
    m3, c3 = np.linalg.lstsq(C, y_new3)[0]
    print(m3, c3)

# ###########################################################################
    f_x = [float(x) * m*0.3 for x in new_reac_x]
    f_y = [float(x) * m2*0.3 for x in new_reac_y]
    f_z = [float(x) * m3*0.3 for x in new_reac_z]

    print('New cell traction forces calculated.')
else:
    print('Unable to calculate the cell traction forces.')
    print('Check the input and output files.')
# ################################################################################

f_x1 = []
f_y1 = []
f_z1 = []
for n in f_x:
    f_x1.append("{0:.4f}".format(n))
for n in f_y:
    f_y1.append("{0:.4f}".format(n))
for n in f_z:
    f_z1.append("{0:.4f}".format(n))

outfile = open('reactions_output.txt', 'w')

for index in range(len(cell_contour)):
    outfile.write(str(cell_contour[index]) + "     " + str(f_x1[index]) + "    " + str(f_y1[index]) + "    " + str(f_z1[index]) + "\n")
outfile.close()

print('\n\n Press Enter to exit...')
