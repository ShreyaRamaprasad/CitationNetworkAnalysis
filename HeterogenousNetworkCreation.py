
# coding: utf-8

# In[1]:


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


# In[2]:


DatasetDirectory = '/Users/shreya/Desktop/UCLA/Capstone/AMinerDatasetAnalysis/dblp-ref/'


# In[3]:


# Load Json
data_as_jsonList = []
count=0

try:
    for file in os.listdir(DatasetDirectory):
        print('Loading File.......'+file)
        f = open(os.path.join(DatasetDirectory,file) , 'r')

        try:
            for line in f:
                data_as_jsonList.append(json.loads(line.strip('\n')))
        except json.JsonDecodeError:
            count+=1

        f.close()
except:
    count+=1
    
if(count!=0):
    print('Error reading %d entries',count)
    
print('Total number of entries:'+str(len(data_as_jsonList)))

# Dump data_as_jsonList into a file
# with open('dataAsJsonList.bin', 'wb') as f:
#     pickle.dump(data_as_jsonList, f)


# In[4]:


# Enable this code when you want to read pickled data_as_jsonList directly
# with open('dataAsJsonList.bin', 'rb') as f:
#     pickle.load(trainTestNodes, f)


# In[4]:


# Author dictionary
author_dictionary = {}
venue_dictionary = {}
year_dictionary = {}
for paper in data_as_jsonList:
    try:
        for a in paper['authors']:
            if a in author_dictionary:
                author_dictionary[a]+=1
            else:
                author_dictionary[a]=1
        if paper['venue'] in venue_dictionary:
            venue_dictionary[paper['venue']] += 1
        else:
            venue_dictionary[paper['venue']] = 1
            
        if paper['year'] in year_dictionary:
            year_dictionary[paper['year']] += 1
        else:
            year_dictionary[paper['year']] = 1
            
            
    except KeyError:
        print('Key error at'+paper['id'])
        
print('Number of authors in the dataset '+ str(len(author_dictionary.keys())))
print('Number of venues in the dataset '+ str(len(venue_dictionary.keys())))
print('Number of years in the dataset '+ str(len(year_dictionary.keys())))


# In[5]:


#  paper ID to node ID mapping.
count = 0
nodeCount=0
paperID2nodeID = {}


for paper in data_as_jsonList:

    
    paperID2nodeID[paper['id']]=nodeCount
    nodeCount+=1

    try:
        for ref in paper['references']:
            if ref not in paperID2nodeID.keys():
                paperID2nodeID[ref]  = nodeCount
                nodeCount+=1  
    except:
        count+=1


print(count)

print('Paper Nodecount ',nodeCount)

#  author ID to node ID mapping.

authorID2nodeID = {}
for author in author_dictionary.keys():
    authorID2nodeID[author]=nodeCount
    nodeCount+=1
    
print('Author Nodecount ',nodeCount)
    
#  venue ID to node ID mapping.
    
venueID2nodeID = {}
for venue in venue_dictionary.keys():
    venueID2nodeID[venue]=nodeCount
    nodeCount+=1
    
print('Venue Nodecount ',nodeCount)


# In[6]:


# with open('paperID2nodeID'+'.bin', 'wb') as f:
#        pickle.dump(paperID2nodeID, f)
# with open('venueID2nodeID'+'.bin', 'wb') as f:
#        pickle.dump(venueID2nodeID, f)
# with open('authorID2nodeID'+'.bin', 'wb') as f:
#        pickle.dump(authorID2nodeID, f)


# In[ ]:


years = [2000,2002,2004,2006,2008,2010,2012,2014,2016]
yearToPaperList = {}


for y in years:
    yearToPaperList[y]=[]
    
for paper in data_as_jsonList:
    year = paper['year']
    
    for y in years:
        if year <= y:
            yearToPaperList[y].append(paper)
            break
            
#sanity check
s=0
for k in yearToPaperList.keys():
#     print(len(yearToPaperList[k]))
    s+= len(yearToPaperList[k])
print(s)


# In[ ]:




# Graph snapshot creation
yearToGraph = {}
yearToNodeList = {}

for y in years:
    yearToNodeList[y] = []
    yearToGraph[y] = nx.DiGraph()

for i in range(len(years)):
    
    print('Creating citation network for year '+str(years[i]))
    
    count=0
    Li = yearToPaperList[years[i]]
    Gr = yearToGraph[years[i]]
    nodes = yearToNodeList[years[i]]
    
    if i !=0:
        Gr.add_edges_from(yearToGraph[years[i-1]].edges())
#         nodes.append(yearToNodeList[years[i-1]])

    for paper in Li:
        u = paperID2nodeID[paper['id']]
        try:
            for ref in paper['references']:
                if ref in paperID2nodeID.keys():
                    v = paperID2nodeID[ref]
                else:
                    print('This should not happen '+str(year))
                    print(paperID2nodeID[paper['id']])
                  
                Gr.add_edge(u,v)
            if paper['references'] != []:
                nodes.append(paperID2nodeID[paper['id']])
        except KeyError:
             count += 1
                
 #   with open('CitationNetwork/CitationNetwork_'+str(years[i])+'.bin', 'wb') as f:
 #       pickle.dump(Gr, f)
        
    with open('CitationNetwork/Nodes_'+str(years[i])+'.bin', 'wb') as f:
        pickle.dump(nodes, f)
        
    if i>1 :
        yearToGraph[years[i-2]]={}
        
      
    
    print('Number of edges of citation network for year '+str(len(Gr.edges())))
       
    print(count)
         


# In[ ]:


# New Papers

# newPapersTargetYears = [2006]

# for targetYear in newPapersTargetYears:

#     targetNodeList = yearToNodeList[targetYear]
   
    
#     with open('CitationNetwork/CitationNetwork_'+str(targetYear)+'.bin', 'rb') as f:
#         targetGraph= pickle.load(f)

#     with open('newPapers/TargetNodeList'+str(targetYear)+'.bin', 'wb') as f:
#         pickle.dump(targetNodeList, f)

#     targetNodeListReferenceDict = {}
#     targetNodeListReferenceList = []

#     for n in targetNodeList:

#         targetNodeListReferenceList.extend(targetGraph.neighbors(n))
#         targetNodeListReferenceDict[n] = targetGraph.neighbors(n)

#     with open('newPapers/targetNodeListReferenceList'+str(targetYear)+'.bin', 'wb') as f:
#         pickle.dump(list(set(targetNodeListReferenceList)), f)

#     with open('newPapers/targetNodeListReferenceDict'+str(targetYear)+'.bin', 'wb') as f:
#         pickle.dump(targetNodeListReferenceDict, f)


# In[ ]:


# Citation Counts: New Papers

# startingYears = [2006,2008,2010]
# targetYears = [[2006,2008,2010],[2008,2010,2012],[2010,2012,2014]]
# targetYearToCitationCounts = {}
# targetYearToCitationCountsPerYear = {}

# for i in range(len(startingYears)):
    
#     startingYear = startingYears[i]
#     targetYear = targetYears[i]
    
#     with open('newPapers/TargetNodeList'+str(startingYear)+'.bin', 'rb') as f:
#         pickle.load(targetNodeList, f)
    
#     for year in targetYear:
#     #     yearToCitationCounts[year] = yearToGraph[year].in_degree(nodeList)
#         targetYearToCitationCounts[year] = {}
#         targetYearToCitationCountsPerYear[year] = {}
        
#         with open('CitationNetwork/CitationNetwork_'+str(year)+'.bin', 'rb') as f:
#             Graph= pickle.load(f)
    
#         for n in targetNodeList:
#             targetYearToCitationCounts[year][n] = Graph.in_degree(n)   
 

#     for year in targetYears:
#         try:
#             if year == startingYear:
#                 targetYearToCitationCountsPerYear[year] = targetYearToCitationCounts[year]
#             else:
#                 for n in targetNodeList:
#                     targetYearToCitationCountsPerYear[year][n] = targetYearToCitationCounts[year][n] - targetYearToCitationCounts[year-2][n]
#         except KeyError:
#             print(year,n)


#     CitationCountsForTargetNodes = {}
#     for n in targetNodeList:
#         CitationCountsForTargetNodes[n] = {}

#     try:
#         for y in targetYear:
#             for n in targetNodeList:
#                 CitationCountsForTargetNodes[n][y] = targetYearToCitationCountsPerYear[y][n]
#     except KeyError:
#         print(y,n)

#     with open('CitationCountsForTargetNodes.bin','wb') as f:
#         pickle.dump(CitationCountsForTargetNodes,f)



# In[ ]:


# with open('targetRefNodesDictionary.bin', 'wb') as f:
#     pickle.dump(targetRefNodesDictionary, f)


# In[ ]:


# with open('CitationCountsForTargetNodes.bin','rb') as f:
#     CitationCountsForTargetNodes = pickle.load(f)


# In[ ]:


# Paper-authorship Paper-venue network

for i in range(len(years)):
    
    print('Creating heterogenous network for year '+str(years[i]))
    
    
    
    with open('CitationNetwork/CitationNetwork_'+str(years[i])+'.bin', 'rb') as f:
        Graph= pickle.load(f)
        
    for j in range(0,i+1):
        
        Li = yearToPaperList[years[j]]

        for paper in Li:
            u = paperID2nodeID[paper['id']]
            try:
                for auth in paper['authors']:
                    v = authorID2nodeID[auth]
                    Graph.add_edge(v,u)
                v = venueID2nodeID[paper['venue']]
                Graph.add_edge(v,u)
            except KeyError:
                print(paper['id'])
                
    nx.write_edgelist(Graph,'HeterogenousNetwork/HeterogenousNetwork_'+str(years[i])+'.txt')
                

    
            
            
    


# In[5]:


# years = [2000,2002,2004,2006,2008,2010,2012,2014,2016]
# for i in range(len(years)):
#     with open('HeterogenousNetwork/HeterogenousNetwork_'+str(years[i])+'.bin', 'rb') as f:
#         Graph= pickle.load(f)
#     nx.write_edgelist(Graph,'HeterogenousNetwork/HeterogenousNetwork_'+str(years[i])+'.txt')
    
    
  

