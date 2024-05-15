# -*- coding: utf-8 -*-
# 
# Created on Tue Dec 11 09:14:10 2018

# @author: S. Hervas
# 
abaqus cae noGUI=Extract_Deformed_config.py 

python3 001_DeleteCell2.py

abaqus cae noGUI='002_Tetra2tri.py' 

python3 003_WritePoly2.py

bash callTetgen.sh

python3 004_tetgen2inp.py

python3 005_interpolate2.py
