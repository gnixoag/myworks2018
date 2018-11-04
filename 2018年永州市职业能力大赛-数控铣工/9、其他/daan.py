# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 08:21:53 2018

@author: gnix_
"""

import os
import sys
import re

src="shijuan.tex"
file="daan.txt"

re1=re.compile(r"{[ABCDabcdtf]}")

with open(src,"r",encoding='UTF-8') as src1:
    b=src1.read()
    c=re1.findall(b)

with open(file,"w",encoding='UTF-8') as file1:
    a=1
    for cc in c:
        file1.write(str(a)+"、")
        cc1=re.sub(r"{|}","",cc)
        file1.write(cc1)
        file1.write("\t")
        if (a%5)==0:
            file1.write("\n")
        if (a % 10)==0:
            file1.write("\n")    
        print(a,cc)
        a=a+1
        
        
        
        
    
