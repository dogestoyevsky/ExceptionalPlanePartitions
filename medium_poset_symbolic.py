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
            
#l = 5; m = 2; 
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
print(promotedOrbits)

m = Symbol('m',int=True)
rushShiPred = []
for M in range(0,rangeTop+1):
    for n in range(1,(int(maxRank)+1+rangeTop)+1):
        if ((M+maxRank+1) % n == 0):       
            [a,b,outPut] = symbolic_poset_functions.rushShiSymbolic(n,tableauIn)
            outPut = sympify(outPut)
            outPut = outPut.subs(m,M)
            rushShiPred += [ M, int((M+maxRank+1)/n), outPut ]

tally = int(len(rushShiPred)/3)
rushShiPred = np.reshape(rushShiPred,[tally,3])
print('M, power of op, number stabilized')
print(rushShiPred)

promotedOrbits = symbolic_poset_functions.promoteOrbitsSymbolic(tableauIn,fullContentOrbits)

#outPutCollect = []
#for M in range(0,6):
#    for n in range(1,(int(maxRank)+1)+1):
#        if ((maxRank+1) % n == 0) & (M % n == 0):
#            outPut= symbolic_poset_functions.collectPromotedOrbits(n,M,tableauIn,promotedOrbits)
#            outPutCollect += [M,int((M+maxRank+1)/n),outPut]
#outPutCollect = np.reshape(outPutCollect,[len(outPutCollect)/3,3],order='C')
#print(outPutCollect)

outPutCollect = []

#M = 3
#rangeTop = 3
#for n in range(1,(int(maxRank)+1+rangeTop)+1):
#    if ((maxRank+1) % n == 0) & (M % n == 0):
#        outPut = symbolic_poset_functions.collectPromotedOrbits(n,M,tableauIn,promotedOrbits)
#            for n2 in range(1,(int(maxRank)+rangeTop+1)+1):
#                if int(outPut[1]) % n2 == 0:
#                    byOrbitDivisibility[M*int(maxRank+1+rangeTop)+n2-1][2] += outPut[0]
# 

#

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

    
print('start')
for M in range(0,rangeTop+1):
#for M in range(0,1):
    for n in range(1,(int(maxRank)+1+rangeTop)+1):
#    for n in [1,11]:
        if ((maxRank+1) % n == 0) & (M % n == 0):
            outPut= symbolic_poset_functions.collectPromotedOrbits(n,M,tableauIn,promotedOrbits)
            outPut = np.reshape(outPut,(int(len(outPut)/2),2))
#            embed()
            for j in range(0,len(outPut)):
#                for n2 in range(1,(int(maxRank)+rangeTop+1)+1):
                    # n2 is coperiod
                    if ((M+maxRank+1) % n == 0) & (((M+maxRank+1)/int(outPut[j][1])) % (n) == 0):
#                        print(['n:',n,'j:',j,'n2:',n2,'Output pd:',outPut[j][1],'no.:',outPut[j][0]])
#                        print(outPut)
                        byOrbitDivisibility[M*int(maxRank+1+rangeTop)+int((M+maxRank+1)/n)-1][2] += outPut[j][0]
                    



print('m,n,total')       
print(byOrbitDivisibility)

# 5/2 morning - Issue: the period may be above the maxmium height. This starts happening for 
# m = 2 (the full-content height 13 poset). Fix this before trying to get predictions to agree/

        # 5/3 morning - resolved issues from yesterday but now I am worried about "collecting" steps - I think I am overcounting.
        # also this is not what I want in the end - want mNum to be symbolic (but mPrime not)