# -*- coding: utf-8 -*-
# 
# Created on Tue Dec 11 09:14:10 2018

# @author: S. Hervas
# 

python 001_DeleteCell.py

abaqus cae noGUI=002_Voxel2tri.py 

python 003_WritePoly.py

tetgen -FYAa0.30S434000 apply_displacements3.poly

python 004_tetgen2inp.py

python 005_interpolate.py
