#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 09:13:43 2017

@author: hollymandel
"""

from sympy import *
import numpy as np
np.set_printoptions(threshold=1000000000)
import math as math
from IPython import embed
import symbolic_poset_functions
            
tableauIn = [1,1,1,2,2,2,2,2,1,1,1]
maxRank = len(tableauIn)-1
fullContentOrbits = [
        [11,1,1],
        [12,3,1],
        [12,12,1],
        [13,13,6],
        [14,7,2],
        [14,14,12],
        [15,15,13],
        [16,2,1],
        [16,4,1],
        [16,8,1],
        [16,16,4]]
rangeTop = 12;


# maxHt, orbit size, number of orbits
promotedOrbits = symbolic_poset_functions.promoteOrbitsSymbolic(tableauIn,fullContentOrbits)
#print(promotedOrbits)

m = Symbol('m',int=True)

#tally = int(len(rushShiPred)/3)
#rushShiPred = np.reshape(rushShiPred,[tally,3])
#print('M, power of op, number stabilized')
#print(rushShiPred)

promotedOrbits = symbolic_poset_functions.promoteOrbitsSymbolic(tableauIn,fullContentOrbits)

byOrbitDivisibility = []
a = 1
b = 0
for M in range(0,rangeTop+1):
    for n in range(0,int(maxRank)+1+rangeTop):
        byOrbitDivisibility += [ b,a,0 ]
        a += 1
        if a == int(maxRank+rangeTop)+2:
            a = 1
            b += 1       
            
byOrbitDivisibility = np.reshape(byOrbitDivisibility,((rangeTop+1)*(int(maxRank)+1+rangeTop),3))    
divByMaxRank = 1

k = 10
byOrbitDivisibility = []
if divByMaxRank:
    possibleD = [1,11] # temporary testing values, here  k = 3
else:
    possibleD = [1]

promotionPred =  symbolic_poset_functions.collectPromotedOrbitsSymbolic(tableauIn,promotedOrbits,divByMaxRank) 
promotionPred = np.reshape(promotionPred,(int(len(promotionPred)/2),2))   


  
##    byOrbitDivisibility += [ possibleD[n], m ]
##byOrbitDivisibility = np.reshape(byOrbitDivisibility,[int(len(byOrbitDivisibility)/2),2])
#rushShiPred = []
#
#outPut = symbolic_poset_functions.collectPromotedOrbitsSymbolic(tableauIn,promotedOrbits,divByMaxRank)
#outPut = np.reshape(outPut,(int(len(outPut)/2),2))
#
rushShiPred = []
for n in [1,11]:
    if (11*k + 11) % n == 0:
        [a,b,outPut] = symbolic_poset_functions.rushShiSymbolic(n,tableauIn)
        rushShiPred += [n, outPut]
rushShiPred = np.reshape(rushShiPred,(int(len(rushShiPred)/2),2))                   
##       
#for n in range(0,len(possibleD)):
#    nNum = possibleD[n]
#    for j in range(0,len(outPut)):
#        byOrbitDivisibility[n][1] += outPut[j][0]
#    byOrbitDivisibility[n][1] += -m



