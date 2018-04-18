# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 15:09:41 2018

@author: swagat
"""
import math

#function to print numbers less than threshhold 
def print_less_than(num_list,threshold):
    print([x  for x in num_list if x<=threshold])
    #print(a)

def is_prime(num):
    num_root = int(math.sqrt(num))
    for n in range(2,num_root):
        if(num%n == 0):
            return False
    
    return True
    
def find_divisors():
    num = int(input("Please enter the number:"))
    div_list = [1,num]
        
    if num == 0:
        print("No divisors possible for 0")
    if num == 1:
        print("Divisors of 1 are [1]")
    
    #quotient = num
    while not is_prime(num):
        for i in range(2,num):
            if num%i == 0:
                num = num/i
                div_list.append(i)
                break
        
        print(num)
        
    
    print(div_list)