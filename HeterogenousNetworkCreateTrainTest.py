
# coding: utf-8

# In[3]:


import pickle
import os
from sklearn.linear_model import LinearRegression 
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import numpy as np


# In[ ]:


embeddingFiles = '/Users/shreya/Desktop/UCLA/Capstone/AMinerDatasetAnalysis/HeterogenousNetworkEmbeddings/HeterogenousNetwork_*.emb'


# In[14]:


targetYear = 2006
targetPrevYears = [2000,2002,2004]


# In[6]:


with open('newPapers/TargetNodeList_'+str(targetYear)+'.bin', 'rb') as f:
    targetNodeList = pickle.load(f)
with open('newPapers/targetNodeListReferenceList'+str(targetYear)+'.bin', 'rb') as f:
    targetNodeListReferenceList = pickle.load(f)
with open('newPapers/targetNodeListReferenceDict'+str(targetYear)+'.bin', 'rb') as f:
    targetNodeListReferenceDict = pickle.load(f)


# In[7]:


print(len(targetNodeList))
print(len(targetNodeListReferenceDict.keys()))
print(len(targetNodeListReferenceList))


# In[12]:


targetNodeList[2]


# In[13]:


targetNodeListReferenceDict[targetNodeList[2]]


# In[ ]:


# Initializing the dictionary
count = 0

targetRefNodesDictionary = {}
for n in targetNodeListReferenceList:
    targetRefNodesDictionary[n] = {}

try:
    for year in targetPrevYears:
        print('Reading for file '+str(year))
        f = open(embeddingFiles.replace('*',str(year)),'r')
        count+=1
        
        firstLine = True

        line_no=0
        for line in f:
            
#             Skip the header in the embedding file
            if firstLine:
                firstLine=False
                continue
                
            line_no+=1
            if line_no%10000==0:
                print(line_no)

            l =list(map(float,line.strip('\n').split(' ')))
#             print(l)
            if int(l[0]) not in targetNodeListReferenceList:
                continue
            else:
#                 trainTestNodesDictionary[(int(l[0]))].extend(l[1:])
                targetRefNodesDictionary[int(l[0])][year] = l[1:]
        
        
except FileNotFoundError:
    print('File not found for the year '+str(year))


# In[ ]:


with open('newPapers/targetRefNodesDictionary'+str(targetYear)+'.bin', 'wb') as f:
    pickle.dump(targetRefNodesDictionary, f)


# In[ ]:


with open('newPapers/CitationCountsForTargetNodes'+str(targetYear)+'.bin','rb') as f:
    CitationCountsForTargetNodes = pickle.load(f)


# In[ ]:


# Create labels for the train test nodes
X = []
y = []

trainPredictPeriods = [([2000], [2006,2008,2010])]

# train_period = [2002,2004,2006,2008,2010]
# predict_period = [2012,2014,2016]

for (train_period,predict_period) in trainPredictPeriods:

    for k in targetNodeList:
        feature = []
        for year in train_period:
            
            avgEmbedding = [0]*32
            numReferences = 0
            
            for v in targetNodeListReferenceDict[k]:
                
                if year in targetRefNodesDictionary[v].keys():
                           
                    avgEmbedding = np.add(avgEmbedding,targetRefNodesDictionary[v][year])
                    numReferences += 1
            if numReferences != 0:
                avgEmbedding = np.divide(avgEmbedding,numReferences)       
            
            
            feature.extend(list(avgEmbedding))
        X.append(feature)


        citation = []
        for year in predict_period:
            citation.extend([CitationCountsForTargetNodes[k][year]])
        y.append(citation)


with open('newPapers/X_'+str(targetYear)+'.bin', 'wb') as f:
    pickle.dump(X, f)
with open('newPapers/y_'+str(targetYear)+'.bin', 'wb') as f:
    pickle.dump(y, f)
