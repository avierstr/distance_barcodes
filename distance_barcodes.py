#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: avierstr

calculate the Levenshtein distances between barcodes and groups them according 
the maximum distance.

"""
import random
from Levenshtein import distance as l_distance
import argparse

#------------------------------------------------------------------------------
def arguments():
    parser = argparse.ArgumentParser(description='Script to calculate Levenshtein \
    distances between sequencing barcodes')
    parser.add_argument('-i', '--input', required=True, 
                        help='Input file in tab delimited format')
    parser.add_argument('-min', '--mindistance', type = int, required=False, default=7,
                        help='Minimum distance.  Default=7')
    parser.add_argument('-max', '--maxdistance', type = int, required=False, default=15,
                        help='Maximum distance.  Default=15')
    args = parser.parse_args()
    return args
#==============================================================================
def distance(A1,A2): 
    distance = l_distance(A1, A2)
    return distance
#==============================================================================
def compl_reverse(self): # take the complement reverse of the sequence 
    inp  = 'ATCG' # translate table for complement
    outp = 'TAGC'
    complement = ''.maketrans(inp, outp)
    R = (self[::-1]).translate(complement)  # complement reverse
    return R
#==============================================================================
def count(resultlist, superset, c): #function to count which barcode to remove
    i = 0 #count number of good comparisons
    for a, b, f, r in resultlist:
        if a in superset and b in superset:
            if f > c:
                i += 1
    return i           
#==============================================================================
def countR(resultlist, superset, c): #function to count which barcode to remove
    i = 0 #count number of good comparisons
    for a, b, f, r in resultlist:
        if a in superset and b in superset:
            if f > c and r > c:
                i += 1
    return i           
#==============================================================================
args = arguments()
infile = args.input
mindist = args.mindistance
maxdist = args.maxdistance

comparelist = []
inputfile = open(infile, "r") 
outputfile = 'barcode_distances.txt'
line = inputfile.readline()
while len(line)>0:
    barcode, seq = line.strip().split('\t')
    comparelist.append([barcode, seq])
    line = inputfile.readline()
inputfile.close()

# compare all barcodes with each other
resultlist = []
y = 0 #position in first range
z = 0 #position in 2nd range
position = 0   
for position in range(position, len(comparelist)-1): 
    z = y
    for position2 in range(position+1,len(comparelist)):
        z +=1
        A1 = comparelist[position][1]
        A2 = comparelist[position2][1]
        diff = distance(A1,A2)   # compare as forward
        diffR = distance(A1,compl_reverse(A2))  # compare as complement reverse
        resultlist.append([comparelist[position][0], comparelist[position2][0], diff, diffR])

of = open(outputfile, 'a')
print('Levenshtein distances between barcodes:', file=of)
for a, b, f, r in sorted(resultlist):
    print(a + ' - ' + b + ' : forw distance: ' + str(f) + ' - compl rev distance: ' + 
          str(r), file=of)

# do several random searches for groups above certain distance values for forward sequences
print('\n-------------------------------------------------------', file=of)
print('Results for comparing only forward sequence of barcodes', file=of)
print('-------------------------------------------------------', file=of)
for limit in range(maxdist, mindist, -1): 
    subset = set()
    for a, b, f, r in resultlist:
        if f > limit: 
            subset.update([a,b])
#            print(a + ' - ' + b + ' : ' + str(f))
    print(sorted(subset))
    i = 0
    randomlist = []
    while i < 5000: # do 5000 random searches
        i += 1
        subset0 = subset.copy()
        random.shuffle(resultlist)
        for a, b, f, r in resultlist:
            if a in subset0 and b in subset0:
                if f > limit:
                    pass
                else:
                    subset1 = subset.copy()
                    subset2 = subset.copy()
                    subset1.remove(a)
                    x = count(resultlist, subset1, limit)
                    subset2.remove(b)
                    y = count(resultlist, subset2, limit)
                    if x > y :
                        subset0.remove(b)
                    else:
                        subset0.remove(a)
       
        randomlist.append(subset0) # save results of xx random replicates in list
        print('random try ' + str(i) + ' for minimum distance of '+ str(limit) +': ' + str(len(subset0)) + ' barcodes' )
    #    print(sorted(subset))
#        for a, b, f, r in sorted(resultlist):
#            if a in subset0 and b in subset0:
#                if f <= limit:
#                    print(a + ' - ' + b + ' : ' + str(f))
    randomlist.sort(key=lambda x : len(x), reverse=True)
    print('Maximum number of barcodes with mutual Levenshtein distance > ' + str(limit) + ': ' + str(len(randomlist[0])))
    print('\nMaximum number of barcodes with mutual Levenshtein distance > ' + str(limit) + ': ' + str(len(randomlist[0])), file=of)
    p = len(randomlist[0])
    randomlist = [i for i in randomlist if len(i) == p] # only keep the longest pools of barcodes
    # check if each pool is unique, remove duplicates
    y = 0 #position in first range
    z = 0 #position in 2nd range
    position = 0   
    for position in range(position, len(randomlist)-1): 
        z = y
        for position2 in range(position+1,len(randomlist)):
            z +=1
            if set(randomlist[position]) == set(randomlist[position2]):
                randomlist[position] = ''           
    randomlist = [x for x in randomlist if x != '']
    
    print('Number of different combinations: ' + str(len(randomlist)))
    print('Number of different combinations: ' + str(len(randomlist)), file=of)
    for x in randomlist:
        print(sorted(x))
        print(sorted(x), file=of)
            
# do several random searches for groups above certain distance values for forward and complement reverse sequences
print('\n-------------------------------------------------------------------------', file=of)
print('Results for comparing forward and complement reverse sequence of barcodes', file=of)
print('-------------------------------------------------------------------------', file=of)
for limit in range(maxdist, mindist, -1): 
    subset = set()
    for a, b, f, r in resultlist:
        if f > limit and r > limit: 
            subset.update([a,b])
#            print(a + ' - ' + b + ' : ' + str(f))
    print(sorted(subset))
    i = 0
    randomlist = []
    while i < 5000: # do 5000 random searches
        i += 1
        subset0 = subset.copy()
        random.shuffle(resultlist)
        for a, b, f, r in resultlist:
            if a in subset0 and b in subset0:
                if f > limit and r > limit:
                    pass
                else:
                    subset1 = subset.copy()
                    subset2 = subset.copy()
                    subset1.remove(a)
                    x = countR(resultlist, subset1, limit)
                    subset2.remove(b)
                    y = countR(resultlist, subset2, limit)
                    if x > y :
                        subset0.remove(b)
                    else:
                        subset0.remove(a)
       
        randomlist.append(subset0) # save results of xx random replicates in list
        print('random try ' + str(i) + ' for minimum distance of '+ str(limit) +': ' + str(len(subset0)) + ' barcodes' )
    #    print(sorted(subset))
#        for a, b, f, r in sorted(resultlist):
#            if a in subset0 and b in subset0:
#                if f <= limit:
#                    print(a + ' - ' + b + ' : ' + str(f))
    randomlist.sort(key=lambda x : len(x), reverse=True)
    print('Maximum number of barcodes with mutual Levenshtein distance > ' + str(limit) + ': ' + str(len(randomlist[0])))
    print('\nMaximum number of barcodes with mutual Levenshtein distance > ' + str(limit) + ': ' + str(len(randomlist[0])), file=of)
    p = len(randomlist[0])
    randomlist = [i for i in randomlist if len(i) == p] # only keep the longest pools of barcodes
    # check if each pool is unique, remove duplicates
    y = 0 #position in first range
    z = 0 #position in 2nd range
    position = 0   
    for position in range(position, len(randomlist)-1): 
        z = y
        for position2 in range(position+1,len(randomlist)):
            z +=1
            if set(randomlist[position]) == set(randomlist[position2]):
                randomlist[position] = ''           
    randomlist = [x for x in randomlist if x != '']
    
    print('Number of different combinations: ' + str(len(randomlist)))
    print('Number of different combinations: ' + str(len(randomlist)), file=of)
    for x in randomlist:
        print(sorted(x))
        print(sorted(x), file=of)
of.close()
print('\nAll results have been saved in the file: ' + outputfile + '\n')