##########################################################################################################
# This file is part of the method that will be soon published in
#
# If you use any part of it, please cite this paper.
###########################################################################################################
import shutil
import tempfile
import math
import re
import numpy as np

l = []
m = []

infile = open('displacements_input2.txt', 'r')

for line in infile:
    li = line.strip()
    if not li.startswith("#"):
        l.append(li.rstrip().split( ))

infile.close()

r = len(l)
print('The number of input nodes with displacements values are:')
print(r)

###############################################################


outfile = open('displac_output_new.txt', 'r')
# outfile = open('displac_output.txt', 'r')

for line in outfile:
    li = line.strip()
    if not li.startswith("#"):
        m.append(li.rstrip().split( ))

outfile.close()

s = len(m)
print('The number of output nodes with displacements values are:')
print(s)

###############################################################


nodes = [row[0] for row in l]

disp_x0 = [row[1] for row in l]
disp_y0 = [row[2] for row in l]
disp_z0 = [row[3] for row in l]
disp_x1 = [row[1] for row in m]
disp_y1 = [row[2] for row in m]
disp_z1 = [row[3] for row in m]

###############################################################

if r == s:

    ErrX = [(float(x) + float(y))  for x, y in zip(disp_x0, disp_x1)]
    ErrY = [(float(x) + float(y))  for x, y in zip(disp_y0, disp_y1)]
    ErrZ = [(float(x) + float(y))  for x, y in zip(disp_z0, disp_z1)]
    
    NormaErrU = [np.sqrt((float(x)**2 + float(y)**2 + float(z)**2)) for x, y, z in zip(ErrX, ErrY, ErrZ)]

    NormaUr = [np.sqrt((float(x) ** 2 + float(y) ** 2 + float(z) ** 2)) for x, y, z in zip(disp_x0, disp_y0, disp_z0)]
    maxDisp = np.max(NormaUr)

    maxError = np.max(NormaErrU)
    error1 = maxError

    print ('The error1 (# Error1: maximo error absoluto) is equal to:')
    print(error1)
    print()
    
    # Error2: media del error
    error2 = np.average(NormaErrU)
    print ('The error2 (# Error2: media del error absoluto) is equal to:')
    print(error2)
    print()
    error2 = np.average(NormaErrU)
    print ('The error2 (# Error2: maximo del error relativo) is equal to:')
    print(error1/maxDisp)
    print()

    disp_x2 = [float(x) + float(y) for x, y in zip(disp_x0, disp_x1)]
    disp_y2 = [float(x) + float(y) for x, y in zip(disp_y0, disp_y1)]
    disp_z2 = [float(x) + float(y) for x, y in zip(disp_z0, disp_z1)]


    new_disp_x = []
    new_disp_y = []
    new_disp_z = []

    for n in disp_x2:
        new_disp_x.append("{0:.6e}".format(n))

    for n in disp_y2:
        new_disp_y.append("{0:.6e}".format(n))

    for n in disp_z2:
        new_disp_z.append("{0:.6e}".format(n))

else:
    print("Unable to evaluate the displacements field.")
    print("Check the input and output displacement files.")

###############################################################


outfile = open('error_nodes.txt', 'w')

for index in range(len(nodes)):
	outfile.write(
		str(nodes[index]) + "     " + str(ErrX[index]) + "    " + str(ErrY[index]) + "    " + str(
			ErrZ[index]) + "\n")
outfile.close()

###############################################################

maxDisp = np.genfromtxt('max_disp.txt')
if np.percentile((NormaErrU),95) > 0.10*maxDisp:

    outfile = open('new_displacements_input.txt', 'w')

    for index in range(len(nodes)):
        outfile.write(
            str(nodes[index]) + "     " + str(new_disp_x[index]) + "    " + str(new_disp_y[index]) + "    " + str(
                new_disp_z[index]) + "\n")
    outfile.close()

    print('The error is greater than 10% of maximun displacement')
    print('The new displacements input file has been created.')

    outfile = open('check_error.txt', 'w')
    outfile.write('1' + '\n')
    outfile.close()

else:
    print('The error is less than 1E-04.')
    print('The output reactions are the cell traction forces.')

    outfile = open('check_error.txt', 'w')
    outfile.write('0' + '\n')
    outfile.close()

print('\n\n Press Enter to exit...')
