# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 12:38:03 2018

@author: Gabriele Nasello
"""
# import matplotlib.pyplot as plt
# import mpl_toolkits.mplot3d as plt3d
# from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import copy

#from profile_support import profile


#@profile
def read_inp(filename):
    """
    Read data from the given INP file.

    Arguments:
        - filename (str)
            filename of the INP file storing a geometry.

    Returns:
        dict
            dictionary with the data load from the INP file.
    """
    # Read INP file's content and remove special \t, \r and \n special
    # characters from it.
    with open(filename, 'rt') as inp_file:
        content = [line.rstrip().replace('\t', '')
                   for line in inp_file.readlines()]

    # Find the headers from the INP file (headers start with a '*')
    headers = [(num_line, line.replace('*', '').lstrip())
               for num_line, line in enumerate(content)
               if line.startswith('*')]

    inpfile = {}

    # Find data associated with each header
    for index, (num_line, header) in enumerate(headers):
        if index < (len(headers) - 1):
            inpfile[header.upper()] = content[num_line+1:headers[index+1][0]]
        else:
            inpfile[header.upper()] = content[num_line+1:] 

    return inpfile;

def remove_header_inp(filename):
    """
    Read data from the given INP file and remove the '*Heading' keyword in the
    first line. This is useful to import single models as parts in Abaqus.

    Arguments:
        - filename (str)
            filename of the INP file storing a geometry.

    Returns:
        dict
            dictionary with the data load from the INP file.
    """
    
    data=read_inp(filename)
    
    if 'HEADING' in data.keys():
        with open(filename, 'r') as fin:
            head, tail = fin.read().split('\n', 1)
        with open(filename, 'w') as fout:
            fout.write(tail)
            
    return;


def get_inp_data(inpfile):
    """
    Read data from the given INP file.

    Arguments:
        - filename (str)
            filename of the INP file storing a geometry.

    Returns:
        dict
            dictionary with the data load from the INP file.
    """
    data=copy.deepcopy(inpfile)
    #Get the nodes identifiers and its associated vertices.
    nodes = []
    for node in data['NODE']:
        node_info = node.split(', ')
        nodes.append([float(vertex) for vertex in node_info])
    data['NODE']=np.asarray(nodes)
    
    # Get the elements identifiers and its associated nodes.
    matching = [s for s in data.keys() if 'ELEMENT, TYPE=' in s]
    for eltype in matching:
        elements = []
        for element in data[eltype]:
            element_info = element.split(',')
            elements.append([int(node) for node in element_info])
        data[eltype]=np.asarray(elements)
    
    # Get the element sets.
    matching = [s for s in data.keys() if 'ELSET, ' in s]
    for elgroup in matching:
        elset = []
        for element in data[elgroup]:
            element_info = element.replace(' ', '').split(',')
            if not element_info[-1]:
                del(element_info[-1])
            elset.extend([int(el) for el in element_info])
        data[elgroup]=np.asarray(elset)
        
    # Get the node sets.
    matching = [s for s in data.keys() if 'NSET, ' in s]
    for nodegroup in matching:
#        print (nodegroup)
        nset=[int(n) for j in data[nodegroup] for n in j.split(',')]
        data[nodegroup]=np.asarray(nset)
        
    # Get the surfaces.
    matching = [s for s in data.keys() if 'SURFACE, ' in s]
    for surfgroup in matching:
        surface = []
        for surf in data[surfgroup]:
            surf_info = surf.replace('S','').split(',')
            surface.append([int(s) for s in surf_info])
        data[surfgroup]=np.asarray(surface)  
    
    return data;

#@profile
def get_nodes(data):
    """
    Get the nodes identifiers and its associated vertices.

    Arguments:
        - data (dict)
            data loaded from the INP file.

    Returns:
        np.ndarray
            array with each row storing a node identifier and its associated
            vertices.
    """
    nodes = []
    for node in data['NODE']:
        node_info = node.split(', ')
        nodes.append([float(vertex) for vertex in node_info])

    return np.asarray(nodes)


#@profile
def get_surface_elements(data):
    """
    Get the elements identifiers and its associated nodes forming a surface
    geometry.

    Arguments:
        - data (dict)
            data loaded from the INP file.

    Returns:
        np.ndarray
            array with each row storing an element identifier and its
            associated vertices.
    """
    elements = []
    for element in data['ELEMENT, TYPE=S3R']:
        element_info = element.split(', ')
        elements.append([int(node) for node in element_info])

    return np.asarray(elements)


#@profile
def get_element_set(data, elements):
    """
    Get the elements identifiers and its associated nodes forming an element 
    set

    Arguments:
        - data (dict)
            data loaded from the INP file.

    Returns:
        np.ndarray
            array with each row storing an element identifier and its
            associated vertices.
    """
    lateral_elements = []
    for element in data['ELSET, ELSET=ES_interface_Scaffold_Bone, GENERATE']:
        element_info = element.split(',')
        first_node = int(element_info[0])
        last_node = int(element_info[1])
        step = int(element_info[2])
        elements_ids = np.arange(first_node, last_node+1, step)

        return elements[np.in1d(elements[:, 0], elements_ids,
                                assume_unique=True), :].astype(int)
        
def get_element_surface(data_set, elements):
    """
    Get the elements identifiers and its associated nodes forming an element 
    surface geometry. The code works only for tetrahedral elements.

    Arguments:
        - data_set (n x 2 matrix, where n is the number of elements of the surface)
            data of the surface loaded from the INP file.

    Returns:
        np.ndarray
            array with each row storing an element identifier and its
            associated vertices.
    """
    
    data_set=data_set[data_set[:,1].argsort()] # sorting rows based on column 1
    #groupby array based on values of colum 1, 
    #assuming the values in the column are always increasing.
    data_set_split=np.split(data_set[:, 0], np.cumsum(np.unique(data_set[:,1], return_counts=True)[1])[:-1])
    
    #'S1':(1,2,3),'S2':(1,2,4),'S3':(2,3,4),'S4':(1,3,4)} 'Surface in .inp file':(nodes connected)
    connectivity=list([[1,2,3],[1,4,2],[2,4,3],[1,3,4]])
    
    elementSet = np.empty((0,3))
    for i in range(len(data_set_split)):
        elementSet=np.vstack((elementSet,elements[data_set_split[i].astype(int)-1,:][:, connectivity[i]]))  
        # indexing first rows, then columns
    
    elementIDnew=(np.arange(elementSet.shape[0])+1).astype(int)
    elementSet=np.hstack((elementIDnew[:, np.newaxis], elementSet)) # adding new elements ID
    
    return elementSet.astype(int);

