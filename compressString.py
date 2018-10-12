# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 10:40:44 2018

@author: swagat
"""

import itertools

myStr = input() 
pStr = ''
for item in [(k,len(list(g))) for k,g in itertools.groupby(myStr)]:
    pStr+=('({0},{1}),'.format(item[0],item[1]))

print(pStr.rstrip(','))
    