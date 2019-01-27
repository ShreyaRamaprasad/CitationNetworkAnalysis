
# coding: utf-8

# In[ ]:


import json
import sys
import os
import pickle
import numpy as np
import random
from matplotlib import pyplot as plt
from networkx.readwrite import json_graph
import networkx as nx
import bisect
import collections

DatasetDirectory = '/Users/shreya/Desktop/UCLA/Capstone/AMinerDatasetAnalysis/dblp-ref/'


newPapersTargetYears = [2006,2008,2010]


for targetYear in newPapersTargetYears:
    
#     with open('HeterogenousNetwork/HeterogenousNetwork_'+str(targetYear)+'.bin', 'rb') as f:
#         targetGraph_directed= pickle.load(f)

    print('Reading File...')
    targetGraph=nx.read_edgelist('HeterogenousNetwork/HeterogenousNetwork_'+str(targetYear)+'.txt')



#     targetNodeList = yearToNodeList[targetYear]

    print('Reading Citation network...')
    with open('CitationNetwork/Nodes_'+str(targetYear)+'.bin', 'rb') as f:
        targetNodeList=pickle.load(f)

    print('Printing Target Nodelist....')
    with open('newPapers/TargetNodeList_'+str(targetYear)+'.bin', 'wb') as f:
        pickle.dump(targetNodeList,f,protocol=2)

    targetNodeListReferenceDict = {}
    targetNodeListReferenceList = []

    for n in targetNodeList:

        targetNodeListReferenceList.extend(targetGraph.neighbors(str(n)))
        targetNodeListReferenceDict[n] = targetGraph.neighbors(str(n))

    print('Writing file 1....')
    with open('newPapers/targetNodeListReferenceList'+str(targetYear)+'.bin', 'wb') as f:
        pickle.dump(list(set(targetNodeListReferenceList)), f,protocol=2)

    print('Writing file 2....')
    with open('newPapers/targetNodeListReferenceDict'+str(targetYear)+'.bin', 'wb') as f:
        pickle.dump(targetNodeListReferenceDict, f,protocol=2)
        


# In[ ]:


# Citation Counts: New Papers

startingYears = newPapersTargetYears
targetYears = [[2006,2008,2010],[2008,2010,2012],[2010,2012,2014]]
targetYearToCitationCounts = {}
targetYearToCitationCountsPerYear = {}

for i in range(len(startingYears)):
    
    startingYear = startingYears[i]
    targetYear = targetYears[i]
    
    with open('newPapers/TargetNodeList_'+str(startingYear)+'.bin', 'rb') as f:
        targetNodeList = pickle.load(f)
    
    for year in targetYear:
    #     yearToCitationCounts[year] = yearToGraph[year].in_degree(nodeList)
        targetYearToCitationCounts[year] = {}
        targetYearToCitationCountsPerYear[year] = {}
        
        with open('CitationNetwork/CitationNetwork_'+str(year)+'.bin', 'rb') as f:
            Graph= pickle.load(f)
    
        print('Reading Citation Network...')

        for n in targetNodeList:
            targetYearToCitationCounts[year][n] = Graph.in_degree(n)   
 

    print('Getting Citation Counts')    

    for year in targetYear:
        try:
            if year == startingYear  :
                targetYearToCitationCountsPerYear[year] = targetYearToCitationCounts[year]
            else:
                for n in targetNodeList:
                    targetYearToCitationCountsPerYear[year][n] = targetYearToCitationCounts[year][n] - targetYearToCitationCounts[year-2][n]
        except KeyError:
            print(year,n)


    print('Inverting the Hash')

    CitationCountsForTargetNodes = {}
    for n in targetNodeList:
        CitationCountsForTargetNodes[n] = {}

    try:
        for y in targetYear:
            for n in targetNodeList:
                CitationCountsForTargetNodes[n][y] = targetYearToCitationCountsPerYear[y][n]
    except KeyError:
        print(y,n)

    print('Dumping Citation Counts')
    with open('newPapers/CitationCountsForTargetNodes'+str(startingYear)+'.bin','wb') as f:
        pickle.dump(CitationCountsForTargetNodes,f)











