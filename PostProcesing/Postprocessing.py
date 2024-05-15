import numpy as np
from FEpy import*
from numpy import array
from scipy.interpolate import griddata
from scipy.interpolate import LinearNDInterpolator
import os

def centeroidnp(arr):
    length, dim = arr.shape
    return np.array([np.sum(arr[:, i])/length for i in range(dim)])
    
numit = len(os.listdir('.\\resultsFolder\\'))
for i in range (0, numit):
	os.system('abaqus viewer noGUI=01_Extract_LE.py -- %i' % (i))
	os.system('abaqus viewer noGUI=01_Extract_U.py -- %i' % (i))

it = 1
num_it = 3


##################################################################################################
# Interpolate strains
##################################################################################################

for it in range (0, num_it+1):
    if it == 0:
        sigma0 = np.genfromtxt('LE_todosElems%i.txt'% (it))
        target0 = 'resultsFolder\\it_%i\\applyReac2\\apply_reactions_2_new.inp' % (it)
        inpfile0 = read_inp(target0)
        data0 = get_inp_data(inpfile0)
        nodes0 = data0['NODE']

        displ0 = np.genfromtxt('displacement_%i.txt' % (int(it)))
        nodesd = np.copy(nodes0)
        nodesd[:,1:4] = nodes0[:,1:4]+displ0[:,1:4]
        conec0 = data0['ELEMENT, TYPE=C3D4']
        centroid0 = np.zeros((len(sigma0),4))
        for i in range(0,len(sigma0)):
            array = np.zeros((4,3))
            array[0,:] = nodesd[conec0[sigma0[i,0].astype(int)-1][1]-1][1:4]
            array[1,:] = nodesd[conec0[sigma0[i,0].astype(int)-1][2]-1][1:4]
            array[2,:] = nodesd[conec0[sigma0[i,0].astype(int)-1][3]-1][1:4]
            array[3,:] = nodesd[conec0[sigma0[i,0].astype(int)-1][4]-1][1:4]
            centroid0[i,0] = sigma0[i,0].astype(int)
            centroid0[i,1:4] = centeroidnp(array)
        
    else:
        sigma0 = sigma_new
        centroid0 = centroid1
        
    if it < num_it:
        sigma1 = np.genfromtxt('LE_todosElems%i.txt'% (it+1))
        target1 = 'resultsFolder\\it_%i\\applyReac2\\apply_reactions_2_new.inp' % (it+1)
        inpfile1 = read_inp(target1)
        data1 = get_inp_data(inpfile1)
        nodes1 = data1['NODE']
        conec1 = data1['ELEMENT, TYPE=C3D4']
        centroid1 = np.zeros((len(sigma1),4))
        for i in range(0,len(sigma1)):
            array = np.zeros((4,3))
            array[0,:] = nodes1[conec1[sigma1[i,0].astype(int)-1][1]-1][1:4]
            array[1,:] = nodes1[conec1[sigma1[i,0].astype(int)-1][2]-1][1:4]
            array[2,:] = nodes1[conec1[sigma1[i,0].astype(int)-1][3]-1][1:4]
            array[3,:] = nodes1[conec1[sigma1[i,0].astype(int)-1][4]-1][1:4]
            centroid1[i,0] = sigma1[i,0].astype(int)
            centroid1[i,1:4] = centeroidnp(array)
               
        sigma_interp_n = griddata(centroid0[:,1:4], sigma0[:,1:7], centroid1[:,1:4], method='nearest')            
        sigma_new = np.zeros((np.shape(sigma1)))
        sigma_new[:,0] = sigma1[:,0]
        sigma_new[:,1:7] = sigma1[:,1:7]+sigma_interp_n[:,0:6]
        # #################### Write vtk
        f = open('cell_def_%i.vtk' %(it), 'w')
        f.write('# vtk DataFile Version 2.0\nPrueba1 \nASCII\n' )
        f.write('DATASET UNSTRUCTURED_GRID\n')
        f.write('POINTS\t%i\tfloat\n' % (len(centroid1)))
        for i in range (0,len(centroid1)):
        	f.write('%10.4F\t%10.4F\t%10.4F\n' % (centroid1[i,1],centroid1[i,2], centroid1[i,3]))     
        f.write('\nCELLS\t%i\t%i\n' % (len(centroid1), len(centroid1)*2))
        for i in range (0, len(centroid1)):
            f.write('1\t%1i\n' % (i))   
#        	f.write('1\t%1i\n' % (nodes1[i,0]-1))   
        f.write('\nCELL_TYPES\t%i\n' % (len(centroid1)))
        for i in range (0, len(centroid1)):
        	f.write('1\n')
        f.write('POINT_DATA %i' % (len(centroid1)))
        f.write('TENSORS cell_def_interp float\n')
        for i in range (0, len(sigma_interp_n)):
            f.write('%10.4F\t%10.4F\t%10.4F\n%10.4F\t%10.4F\t%10.4F\n%10.4F\t%10.4F\t%10.4F\n\n' % (sigma_interp_n[i,0], sigma_interp_n[i,3], sigma_interp_n[i,4], sigma_interp_n[i,3], sigma_interp_n[i,1], sigma_interp_n[i,5], sigma_interp_n[i,4], sigma_interp_n[i,5], sigma_interp_n[i,2]))
        f.write('TENSORS cell_def_suma float\n')
        for i in range (0, len(sigma_interp_n)):
            f.write('%10.4F\t%10.4F\t%10.4F\n%10.4F\t%10.4F\t%10.4F\n%10.4F\t%10.4F\t%10.4F\n\n' % (sigma_new[i,1], sigma_new[i,4], sigma_new[i,5], sigma_new[i,4], sigma_new[i,2], sigma_new[i,6], sigma_new[i,5], sigma_new[i,6], sigma_new[i,3]))
        f.close()
        # ################################################        
    else:
        np.savetxt('le_final_t.txt', sigma_new, fmt='%i\t%10.7e\t%10.7e\t%10.7e\t%10.7e\t%10.7e\t%10.7e')

# #################### Write vtk
f = open('cell_def_final.vtk', 'w')
f.write('# vtk DataFile Version 2.0\nPrueba1 \nASCII\n' )
f.write('DATASET UNSTRUCTURED_GRID\n')
f.write('POINTS\t%i\tfloat\n' % (len(centroid1)))
for i in range (0,len(centroid1)):
	f.write('%10.4F\t%10.4F\t%10.4F\n' % (centroid1[i,1],centroid1[i,2], centroid1[i,3]))     
f.write('\nCELLS\t%i\t%i\n' % (len(centroid1), len(centroid1)*2))
for i in range (0, len(centroid1)):
    f.write('1\t%1i\n' % (i))   
f.write('\nCELL_TYPES\t%i\n' % (len(centroid1)))
for i in range (0, len(centroid1)):
	f.write('1\n')
f.write('POINT_DATA %i' % (len(centroid1)))
f.write('TENSORS cell_def_suma float\n')
for i in range (0, len(sigma_interp_n)):
    f.write('%10.4F\t%10.4F\t%10.4F\n%10.4F\t%10.4F\t%10.4F\n%10.4F\t%10.4F\t%10.4F\n\n' % (sigma_new[i,1], sigma_new[i,4], sigma_new[i,5], sigma_new[i,4], sigma_new[i,2], sigma_new[i,6], sigma_new[i,5], sigma_new[i,6], sigma_new[i,3]))
f.close()


#Averaging stresses in nodes in last mesh
it = 3
sigma_ele = np.genfromtxt('le_final_t.txt')
target1 = 'resultsFolder\\it_%i\\applyReac2\\apply_reactions_2_new.inp' % (it)
inpfile1 = read_inp(target1)
data1 = get_inp_data(inpfile1)
nodes1 = data1['NODE']
conec1 = data1['ELEMENT, TYPE=C3D4']
nodes_surface = data1['NSET, NSET=NODOS_SURFACE_CYTO']
elem = data1['ELSET, ELSET=ELEMENT_CYTO']
conect = np.zeros((len(elem),5))
for i in range (0, len(elem)):
	conect[i,0] = elem[i]
	conect[i,1:5] = conec1[elem[i]-1,1:5]
    
sigma_nodos = np.zeros((len(nodes_surface),7))
for i in range (len(nodes_surface)):
    tensiones = sigma_ele[np.argwhere(nodes_surface[i]==conect[:,1:5])[:,0],:]
    sigma_nodos[i,0] = nodes_surface[i]
    sigma_nodos[i,1] = np.mean(tensiones[:,1])
    sigma_nodos[i,2] = np.mean(tensiones[:,2])
    sigma_nodos[i,3] = np.mean(tensiones[:,3])
    sigma_nodos[i,4] = np.mean(tensiones[:,4])
    sigma_nodos[i,5] = np.mean(tensiones[:,5])
    sigma_nodos[i,6] = np.mean(tensiones[:,6])

np.savetxt('le_final_nodos.txt', sigma_nodos, fmt='%i\t%10.7e\t%10.7e\t%10.7e\t%10.7e\t%10.7e\t%10.7e')


##################################################################################################
# Recover the stress
##################################################################################################
d_1 = 0.005
c_10 = 20

target1 = 'directo_amp_S.inp' 
le = np.genfromtxt('le_final_nodos.txt')
normals = np.genfromtxt('normals.txt')
sigma_p = np.zeros_like(le)
sigma_xyz = np.zeros_like(le)
sigma_vt = np.zeros_like(le)
sigma_it = np.zeros_like(le)
d_total = np.zeros_like(le)
ne_total = np.zeros_like(le)
t_total = np.zeros((len(le),3))
j_t =np.zeros(len(le))
sigma_p[:,0] = le[:,0]
sigma_xyz[:,0] = le[:,0]
for i in range (0, len(le)):

    le_n = np.zeros((3,3))
    le_n[0,0] = le[i,1]
    le_n[1,1] = le[i,2]
    le_n[2,2] = le[i,3]
    le_n[0,1] = le[i,4]*0.5
    le_n[1,0] = le[i,4]*0.5
    le_n[0,2] = le[i,5]*0.5
    le_n[2,0] = le[i,5]*0.5
    le_n[1,2] = le[i,6]*0.5
    le_n[2,1] = le[i,6]*0.5

    w, v = np.linalg.eig(le_n) 
    le_p = np.zeros((3,3))
    a = np.sort(w)
    le_p[0,0] = a[2]
    le_p[1,1] = a[1]
    le_p[2,2] = a[0]

    r_t = np.zeros((3,3))

    r_t[:, 0] = v[:,np.argwhere(w==le_p[0,0])].reshape((3,))
    r_t[:, 1] = v[:,np.argwhere(w==le_p[1,1])].reshape((3,))
    r_t[:, 2] = v[:,np.argwhere(w==le_p[2,2])].reshape((3,))
    r = np.transpose(r_t)

    e_d = np.zeros((3,3))
    e_d[0,0] = np.exp(le_p[0,0])
    e_d[1,1] = np.exp(le_p[1,1])
    e_d[2,2] = np.exp(le_p[2,2])
    e_le = e_d  
    ne = e_le - np.eye(3)

    b= np.dot(e_le,e_le)

    j = np.sqrt(np.linalg.det(b))

    b_g = np.multiply(j**(-2/3),b)

    i_1 = np.sum(np.diag(b_g))

    sigma_v = 2/d_1*(j-1)*np.eye(3)
    sigma_i = np.multiply(2*c_10/j,b_g - np.multiply(i_1/3,np.eye(3)))
    sigma = sigma_v + sigma_i
    sigma_n_xyz = np.dot(r_t,np.dot(sigma,r))
    
    t = np.zeros(3)
    t_n = np.dot(sigma_n_xyz,np.transpose(normals[i,1:4]))
    t_total[i] = t_n

    sigma_vt[i,0] = sigma_v[0,0]
    sigma_vt[i,1] = sigma_v[1,1] 
    sigma_vt[i,2] = sigma_v[2,2]
    sigma_vt[i,3] = sigma_v[0,1] 
    sigma_vt[i,4] = sigma_v[0,2] 
    sigma_vt[i,5] = sigma_v[1,2]
    
    sigma_it[i,0] = sigma_i[0,0]
    sigma_it[i,1] = sigma_i[1,1] 
    sigma_it[i,2] = sigma_i[2,2]
    sigma_it[i,3] = sigma_i[0,1] 
    sigma_it[i,4] = sigma_i[0,2] 
    sigma_it[i,5] = sigma_i[1,2]
    
    sigma_p[i,1] = sigma[0,0]
    sigma_p[i,2] = sigma[1,1] 
    sigma_p[i,3] = sigma[2,2]
    sigma_p[i,4] = sigma[0,1] 
    sigma_p[i,5] = sigma[0,2] 
    sigma_p[i,6] = sigma[1,2] 
    
    sigma_xyz[i,1] = sigma_n_xyz[0,0]
    sigma_xyz[i,2] = sigma_n_xyz[1,1] 
    sigma_xyz[i,3] = sigma_n_xyz[2,2]
    sigma_xyz[i,4] = sigma_n_xyz[0,1] 
    sigma_xyz[i,5] = sigma_n_xyz[0,2] 
    sigma_xyz[i,6] = sigma_n_xyz[1,2] 
    
    d_total[i,0] = le_p[0,0]
    d_total[i,1] = le_p[1,1] 
    d_total[i,2] = le_p[2,2]
    d_total[i,3] = le_p[0,1] 
    d_total[i,4] = le_p[0,2] 
    d_total[i,5] = le_p[1,2]
    
    ne_total[i,0] = ne[0,0]
    ne_total[i,1] = ne[1,1] 
    ne_total[i,2] = ne[2,2]
    ne_total[i,3] = ne[0,1] 
    ne_total[i,4] = ne[0,2] 
    ne_total[i,5] = ne[1,2]

    j_t[i] = j
    
nodes1 = np.genfromtxt('nodes.txt')
conec1 = np.genfromtxt('conec.txt')
nodes_surface = np.genfromtxt('nodos_surface_cell.txt')
elem = np.arange(  17425,  193086,       1)
conect = np.zeros((len(elem),5))
for i in range (0, len(elem)):
	conect[i,0] = elem[i]
	conect[i,1:5] = conec1[elem[i]-1,1:5]
    
f = open('cell_stress_directo_v.vtk', 'w')
f.write('# vtk DataFile Version 2.0\nPrueba1 \nASCII\n' )
f.write('DATASET UNSTRUCTURED_GRID\n')
f.write('POINTS\t%i\tfloat\n' % (len(nodes1)))
for i in range (0,len(nodes1)):
	f.write('%10.4F\t%10.4F\t%10.4F\n' % (nodes1[i,1],nodes1[i,2], nodes1[i,3]))
f.write('\nCELLS\t%i\t%i\n' % (len(conec1), len(conec1)*5))
for i in range (0, len(conec1)):
	f.write('4\t%1i\t%i\t%i\t%i\n' % (conec1[i,1]-1,conec1[i,2]-1, conec1[i,3]-1, conec1[i,4]-1))
f.write('\nCELL_TYPES\t%i\n' % (len(conec1)))
for i in range (0, len(conec1)):
	f.write('10\n')
nodes_cell = np.genfromtxt('nodos_cell.txt')
f.write('\nCELL_DATA %i\nPOINT_DATA %i\nSCALARS cell float\nLOOKUP_TABLE cell\n' %(len(conec1),len(nodes1)))
for i in range (1, len(nodes1)+1):
    if i in nodes_cell:
       f.write('1\n')
    else:
        f.write('0\n')
f.write('\nCELL_DATA %i\nPOINT_DATA %i\nSCALARS j float\nLOOKUP_TABLE cell\n' %(len(conec1),len(nodes1)))
for i in range (1, len(nodes1)+1):
    if i in nodes_surface:
       pos = np.argwhere(nodes_surface==i)
       f.write('%10.6e\n' % (j_t[pos]))
    else:
        f.write('0.0\n')
f.write('VECTORS cell_tractions float\n')
for i in range (1, len(nodes1)+1):
    if i in nodes_surface:
       pos = np.argwhere(nodes_surface==i)
       f.write('%10.6e\t %10.6e\t %10.6e\n' % (t_total[pos,0],t_total[pos,1],t_total[pos,2]))
    else:
        f.write('0.0\t 0.0\t 0.0\n')
f.write('TENSORS cell_stress_ppal float\n')
for i in range (1, len(nodes1)+1):
    if i in nodes_surface:
       pos = np.argwhere(nodes_surface==i)
       f.write('%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n\n' % (sigma_p[pos,1], sigma_p[pos,4], sigma_p[pos,5], sigma_p[pos,4], sigma_p[pos,2], sigma_p[pos,6], sigma_p[pos,5], sigma_p[pos,6], sigma_p[pos,3]))
    else:
        f.write('0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n\n')
f.write('TENSORS cell_stress_xyz float\n')
for i in range (1, len(nodes1)+1):
    if i in nodes_surface:
       pos = np.argwhere(nodes_surface==i)
       f.write('%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n\n' % (sigma_xyz[pos,1], sigma_xyz[pos,4], sigma_xyz[pos,5], sigma_xyz[pos,4], sigma_xyz[pos,2], sigma_xyz[pos,6], sigma_xyz[pos,5], sigma_xyz[pos,6], sigma_xyz[pos,3]))
    else:
        f.write('0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n\n')
f.write('TENSORS cell_sigma_v float\n')
for i in range (1, len(nodes1)+1):
    if i in nodes_surface:
       pos = np.argwhere(nodes_surface==i)
       f.write('%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n\n' % (sigma_vt[pos,0], sigma_vt[pos,3], sigma_vt[pos,4], sigma_vt[pos,3], sigma_vt[pos,1], sigma_vt[pos,5], sigma_vt[pos,4], sigma_vt[pos,5], sigma_vt[pos,2]))
    else:
        f.write('0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n\n')
f.write('TENSORS cell_sigma_i float\n')
for i in range (1, len(nodes1)+1):
    if i in nodes_surface:
       pos = np.argwhere(nodes_surface==i)
       f.write('%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n\n' % (sigma_it[pos,0], sigma_it[pos,3], sigma_it[pos,4], sigma_it[pos,3], sigma_it[pos,1], sigma_it[pos,5], sigma_it[pos,4], sigma_it[pos,5], sigma_it[pos,2]))
    else:
        f.write('0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n\n')
f.write('TENSORS cell_le_ppal float\n')
for i in range (1, len(nodes1)+1):
    if i in nodes_surface:
       pos = np.argwhere(nodes_surface==i)
       f.write('%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n\n' % (d_total[pos,0], d_total[pos,3], d_total[pos,4], d_total[pos,3], d_total[pos,1], d_total[pos,5], d_total[pos,4], d_total[pos,5], d_total[pos,2]))
    else:
        f.write('0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n\n')
        
f.write('TENSORS cell_ne float\n')
for i in range (1, len(nodes1)+1):
    if i in nodes_surface:
       pos = np.argwhere(nodes_surface==i)
       f.write('%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n\n' % (ne_total[pos,0], ne_total[pos,3], ne_total[pos,4], ne_total[pos,3], ne_total[pos,1], ne_total[pos,5], ne_total[pos,4], ne_total[pos,5], ne_total[pos,2]))
    else:
        f.write('0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n\n')

f.write('TENSORS abaqus float\n')
for i in range (1, len(nodes1)+1):
    if i in nodes_surface:
       pos = np.argwhere(nodes_surface==i)
       f.write('%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n%10.6e\t%10.6e\t%10.6e\n\n' % (le[pos,1], le[pos,4], le[pos,5], le[pos,4], le[pos,2], le[pos,6], le[pos,5], le[pos,6], le[pos,3]))

    else:
        f.write('0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n0.0\t0.0\t0.0\n\n')
f.close()   

