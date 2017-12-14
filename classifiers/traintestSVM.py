import numpy as np
from operator import itemgetter
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
import csv

# training and cross validation
with open('data/processed_tfidf/ALLYEARS/SPARSE2016.dat') as f:
    content = f.readlines()

data = []
for line in content:
   y = int(line.split()[0]) # get spam spam_classification
   wtemp = line.split()[1:] # get word counts

   w = []
   for i in range(0, len(wtemp)):
      w.append((wtemp[i].split(":")[0], wtemp[i].split(":")[1]))
   data.append((y, w))

X = np.zeros((len(data), 16244)) # matrix indexed by cmat[di-1][wj]
Y = np.zeros(len(data))

for i in range(0, len(data)):
   Y[i] = data[i][0]
   for feat, fval in data[i][1]:
      X[i-1][int(feat)] = float(fval)

print np.array(Y).shape
print np.matrix(X).shape

svm_sm = LinearSVC(C=0.5, random_state=42, loss='hinge')
svm_sm.fit(X, Y)
scores = cross_val_score(svm_sm, X, Y, cv=5)

print scores.mean()

# testing
with open('data/processed_tfidf/ALLYEARS/SPARSE2008.dat') as f:
    content = f.readlines()

data = []
for line in content:
   y = int(line.split()[0]) # get spam spam_classification
   wtemp = line.split()[1:] # get word counts

   w = []
   for i in range(0, len(wtemp)):
      w.append((wtemp[i].split(":")[0], wtemp[i].split(":")[1]))
   data.append((y, w))

Xtest = np.zeros((len(data), 16244)) # matrix indexed by cmat[di-1][wj]
Ytest = np.zeros(len(data))

for i in range(0, len(data)):
   Ytest[i] = data[i][0]
   for feat, fval in data[i][1]:
      Xtest[i-1][int(feat)] = float(fval)

print np.array(Ytest).shape
print np.matrix(Xtest).shape

feature_predict = svm_sm.predict(Xtest)

ncorrect = 0
for i in range(0, len(Ytest)):
   if (Ytest[i] == feature_predict[i]):
      ncorrect += 1

accuracy = float(ncorrect)/len(Ytest)

print accuracy

