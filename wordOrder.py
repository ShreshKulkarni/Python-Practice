# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 11:32:06 2018

@author: swagat
"""
import itertools

num_words = input()
list_words = []
while(True):
    word=input()
    if word:
        list_words.append(word)
    else:
        break;

dict_words = {}    
for word in list_words:
    if dict_words.get(word) is None:
        dict_words[word] = 1
    else:
        dict_words[word] += 1
        
print(list(dict_words.values()),sep=' ')