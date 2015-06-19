
# coding: utf-8

# In[1]:


# In[2]:

import sklearn.preprocessing
import numpy as np
import collections
import copy
from sklearn import metrics
from random import randint
from sklearn.cluster import AffinityPropagation


evaluation = open('./result_evaluation_chapiter','w')

para_1 = [round(x,2) for x in np.arange(0.5,1,0.05).tolist()]    #damping
para_2 = []     #max_iter
for i in range(2,200):
    para_2.append(i)
para_3 = []     #convergence_iter
for i in range(1,15):
    para_3.append(i)
para_4 = [True]     #copy
para_5 = ['euclidean', 'precomputed']
para_6 = [False]



# Similarité entre les personnages

# In[3]:

#f = open('./feature','r')
f_2 = open('./feature_chapiter','r')
#X = []
X_2 = []
#for line in f:
#    temp = map(float, line.replace('[','').replace(']','').split(',')[:])
#    X.append(temp)
for line in f_2:
    temp = map(float, line.replace('[','').replace(']','').split(',')[:])
    X_2.append(temp)

f_2.close()

#X = np.array(X)
X_2 = np.array(X_2)
    
#nX = sklearn.preprocessing.normalize(X, norm='l2', axis=1, copy=True)
nX_2 = sklearn.preprocessing.normalize(X_2, norm='l2', axis=1, copy=True)

#X = []
#for i in range(len(nX)):
#    X.append([])
#    for t in nX[i]:
#        X[i] = np.append(X[i], [t])
#    for c in nX_2[i]:
#        X[i] = np.append(X[i], [c])
#X = np.array(X)
X = np.array(nX_2)



name = open('./result','r')
ps = []
for line in name:
    person = line.split('      ')[0]
    ps.append(person)
    
name.close()

f = open('./annotation_name','r')
truth = []
n = 0
for line in f:
    truth.append([])
    truth[n] = line.split('\n')[0].split(',')
    n = n + 1

f.close()

A = np.dot(X, X.T)

def findnext(current,i):
    return [x[0] for x in frequency[i].most_common(len(frequency[i].keys()))].index(current)+1

def notinlist(current,i):
    return current not in frequency[i].most_common(len(frequency[i].keys()))

n = 0.
for p_1 in para_1:
    for p_2 in para_2:
        print ('progress:     '+str(round(n/len(para_1)/len(para_2), 4)*100)+'%\n')
        for p_3 in para_3:
            for p_4 in para_4:
                for p_5 in para_5:
                    for p_6 in para_6:
                        af = AffinityPropagation(damping=p_1, max_iter=p_2, convergence_iter=p_3, copy=p_4, preference=None, affinity=p_5, verbose=p_6).fit(A)
                        cluster_centers_indices = af.cluster_centers_indices_
                        labels = af.labels_
                        try:
                            n_clusters_ = len(cluster_centers_indices)
                        except TypeError:
                            continue


                        pred = []
                        for i in range(n_clusters_):
                            pred.append([])
                        for i in range(len(ps)):
                            pred[labels[i]].append(ps[i])


                        index_truth = []
                        for obj in pred:
                            temp = []
                            for element in obj:
                                for i in range(len(truth)):
                                    if element in truth[i]:
                                        temp.append(i)
                            index_truth.append(temp)

                        frequency = [collections.Counter(x) for x in index_truth]

                        temp = [x.most_common(1)[0][0] for x in frequency]

                        while len(temp) != len(set(temp)):
                            for i in range(len(temp)):
                                for j in range(len(temp)):
                                    if i!=j and temp[i]==temp[j]:
                                        if findnext(temp[i],i) >= len(frequency[i].most_common(len(frequency[i].keys()))) and findnext(temp[j],j) >= len(frequency[j].most_common(len(frequency[j].keys()))):         #both 2 lists reach the end
                                            while temp[i] in (temp[:i] + temp[(i + 1):]):
                                                temp[i] = randint(0,len(truth)+1)
                                                
                                        elif notinlist(temp[i],i) or findnext(temp[i],i) >= len(frequency[i].most_common(len(frequency[i].keys()))):     #frequency[i] reaches its end
                                            if temp[j] not in frequency[j].most_common(len(frequency[j].keys())):
                                                while temp[j] in (temp[:j] + temp[(j + 1):]):
                                                    temp[j] = randint(0,len(truth)+1)
                                            else:
                                                temp[j] = frequency[j].most_common(len(frequency[j].keys()))[findnext(temp[j],j)][0]
                                            
                                        elif notinlist(temp[j],j) or findnext(temp[j],j) >= len(frequency[j].most_common(len(frequency[j].keys()))):
                                            if temp[i] not in frequency[i].most_common(len(frequency[i].keys())):
                                                while temp[i] in (temp[:i] + temp[(i + 1):]):
                                                    temp[i] = randint(0,len(truth)+1)
                                            else:
                                                temp[i] = frequency[i].most_common(len(frequency[i].keys()))[findnext(temp[i],i)][0]
                                            
                                        elif frequency[i].most_common(len(frequency[i].keys()))[findnext(temp[i],i)][1] + temp[j] <= frequency[j].most_common(len(frequency[j].keys()))[findnext(temp[j],j)][1] + temp[i]:
                                            temp[j] = frequency[j].most_common(len(frequency[j].keys()))[findnext(temp[j],j)][0]
                                            
                                        elif frequency[i].most_common(len(frequency[i].keys()))[findnext(temp[i],i)][1] + temp[j] > frequency[j].most_common(len(frequency[j].keys()))[findnext(temp[j],j)][1] + temp[i]:
                                            temp[i] = frequency[i].most_common(len(frequency[i].keys()))[findnext(temp[i],i)][0]

                        index_pred = copy.deepcopy(index_truth)

                        for i in range(len(index_truth)):
                            for j in range(len(index_truth[i])):
                                index_pred[i][j] = temp[i]

                        labels_true = []
                        labels_pred = []
                        for i in range(len(index_truth)):
                            labels_true = labels_true + index_truth[i]
                            labels_pred = labels_pred + index_pred[i]
                            

                        evaluation.write('damping='+str(p_1)+', max_iter='+str(p_2)+', convergence_iter='+str(p_3)+', copy='+str(p_4)+', preference=None, affinity='+str(p_5)+', verbose='+str(p_6)+'\n')
                        evaluation.write(str(metrics.adjusted_rand_score(labels_true, labels_pred))+'\n')
                        evaluation.write(str(metrics.adjusted_mutual_info_score(labels_true, labels_pred)))
                        evaluation.write('\n\n')

        n = n+1

evaluation.close()