# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 13:08:18 2018

@author: swagat
"""
import time

f = open("C:\\Users\\swagat\\Desktop\\input03.txt")

iArr = []
for line in f.readlines():
    iArr.append(list(map(int, line.rstrip('\n').split(' '))));
    
print(iArr[0])
print(len(iArr[1]))
print(len(iArr[2]))
print(len(iArr[3]))

stTime = time.time()
#converting the list to set is the real time saver. The x in A will take humongous time if this is not done
A = set(iArr[2])
B = set(iArr[3])
happy=len([x for x in iArr[1] if x in A])
sad=len([i for i in iArr[1] if i in B])
print( happy, sad, happy-sad)

print(time.time() - stTime)
