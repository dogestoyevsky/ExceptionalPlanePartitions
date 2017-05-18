#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 14:55:10 2017

@author: hollymandel
"""
from sympy import *
import numpy as np
import math as math
from IPython import embed

# want tableau-describing input to be array of multiplicities
def rushShiSymbolic(ord,tableauIn):
    # ord is the order of action - reciprocal to period
    topList = Symbol('topList',int=True)
    topList = 1
    bottomList = 1
    m = Symbol('m',int=true)
    maxRank = len(tableauIn) - 1
    topSum = 0
    bottomSum = 0
    
    t = 0
    while t*ord < maxRank+1:
        downExponent = int(tableauIn[(maxRank+1)-t-1])
        topList *= (m+maxRank+1-t*ord)**downExponent
        topSum += downExponent
        t += 1
    t = 1
    while t*ord <= maxRank+1:
        upExponent = int(tableauIn[t-1])
        bottomList *= (t*ord)**upExponent
        bottomSum += upExponent      
        t += 1  
    
    if topSum > bottomSum:
        outPut = 0
    else:
        outPut = topList / bottomList
    return topList, bottomList, outPut

#N = desired max ht, tableauMaxHt
def promoteOrbitsSymbolic(tableauIn,fullContentOrbits): 
    # Since our two varieties of interest have prime maximum rank, I am only 
    # writing in the case where d = 1 and d = maxRank and having it give out 
    # inputs for either case. The difference will be determined by hand in
    # the collectPromotedOrbits stage
    maxRank = len(tableauIn)-1
    m = Symbol('m',int=true)
    N = m + maxRank + 1
    contentLength = len(fullContentOrbits)  
    promotedOrbits = []
    alytPrediction = []    
    for j in range(0,contentLength):
        maxHt = fullContentOrbits[j][0]
        orbitSize = fullContentOrbits[j][1]
        numOrbits = fullContentOrbits[j][2]
        for d in [1,maxRank+1]:
            straightShape = np.ones([maxHt,1], dtype=int, order='C')
            [ topList,bottomList,numContentVectors ] = rushShiSymbolic(d,straightShape)
            # number stabilized by N/dth power of the operation
            # N/d = tc
            numTableauxNumerator = topList * int(orbitSize) * int(numOrbits)
            numTableauxDenominator = bottomList
            promotedPeriod = orbitSize * (N/d) / gcd(int(maxHt/d),int(orbitSize))
            promotedOrbits += [ promotedPeriod, numTableauxNumerator, numTableauxDenominator, d, j+1, maxHt ]
            # the fifth entry is the total height the tableaux would need to be ("maximum label value")
            # for this orbit to be able to show up. 
    numRows = int(len(promotedOrbits)/6)
    promotedOrbits = np.reshape(promotedOrbits,[numRows,6], order='C')    
    return promotedOrbits

# I don't think this part can reasonably be run symbolically. This would require
# narrowing down the divisibility cases.

# To simplify: set fixed m and desired n
def collectPromotedOrbits(n,mNum,tableauIn,promotedOrbits):
    # goal: get the data into the same form as the Rush-Shi prediction. So, for every 
    # d, find out how many tableaux corresponding to that coperiod d 
    m = Symbol('m',int=True)
    maxRank = len(tableauIn)-1
    numPromotedOrbits = len(promotedOrbits);
    N = mNum + maxRank + 1
    thisNum = 0
    thisDenom = 0
    outPut = []
    for k in range(0,numPromotedOrbits):
        heightOfThisOrbit = promotedOrbits[k][5]
        mPrime = mNum - (heightOfThisOrbit - (maxRank+1))
        if (mNum + maxRank + 1) >= heightOfThisOrbit:
            getDivisor = promotedOrbits[k][3]
            if getDivisor == n: 
                # this is gross! fix!
                getPd = promotedOrbits[k][0]
                getPd = sympify(getPd)
                evalPd = getPd.subs(m,mNum) # WHY USE MNUM HERE, MPRIME ELSEWHERE?
                getTableauxNumerator = promotedOrbits[k][1]
                getTableauxDenominator = promotedOrbits[k][2]   
                getTableauxNumeratorSymb = sympify(getTableauxNumerator)
                evalTableaux = getTableauxNumeratorSymb.subs(m,mPrime) / getTableauxDenominator
                outPut += [ evalTableaux, evalPd ]
                
    return outPut

def collectPromotedOrbitsSymbolic(tableauIn,promotedOrbits,divByMaxRank):
    # goal: get the data into the same form as the Rush-Shi prediction. So, for every 
    # d, find out how many tableaux corresponding to that coperiod d 
    m = Symbol('m',int=True)
    maxRank = len(tableauIn)-1
    numPromotedOrbits = len(promotedOrbits);
    N = m + maxRank + 1
    thisNum = 0
    thisDenom = 0
    outPut = []
    for k in range(0,numPromotedOrbits):
        heightOfThisOrbit = promotedOrbits[k][5]
        mPrime = Symbol('mPrime',int=True)
        mPrime = m - (heightOfThisOrbit - (maxRank+1))
        # assume m large enough that all orbits included
        if divByMaxRank:
            possibleD = [1,maxRank+1]
        else:
            possibleD = [1]
                
        for n in possibleD:
            getDivisor = promotedOrbits[k][3]
            if getDivisor == n: 
                getPd = promotedOrbits[k][0]
                evalPd = sympify(getPd)
                getTableauxNumerator = promotedOrbits[k][1]
                getTableauxDenominator = promotedOrbits[k][2]   
                getTableauxNumeratorSymb = sympify(getTableauxNumerator)
                evalTableaux = getTableauxNumeratorSymb.subs(m,mPrime) / getTableauxDenominator
                outPut += [ evalTableaux, evalPd ]
            
    return outPut