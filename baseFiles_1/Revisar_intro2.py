# -*- coding: utf-8 -*-
"""
Created on Fri May  3 09:24:16 2019

@author: Silvia
"""

import numpy as np
import os

cnt = 1
with open('apply_reactions_2_new.inp', 'r') as file:
	for line in file:
		cnt += 1
		if '*Cload' in line:
			matchedLine = line
			Cload_line = cnt 
			break
       
l = []
infile = open('apply_reactions_2_new.inp', 'r')
for line in infile:
    li=line.strip()
    if not li.startswith("#"):
        l.append(li.rstrip().split())
infile.close()

if l[cnt-1] == []:
    cnt2 = 0
    with open("apply_reactions_2_new.inp", "r") as input:
        with open("apply_reactions_2_new2.inp", "w") as output:
            for line in input:
                cnt2 += 1
                if cnt2 != Cload_line:
                    output.write(line)
    os.remove("apply_reactions_2_new.inp")
    os.rename('apply_reactions_2_new2.inp', 'apply_reactions_2_new.inp')