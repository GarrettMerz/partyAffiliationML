# Author: Rory Fitzpatrick
# Quick implementation of scikit logistic regression using
# five-fold cross validation

import numpy as np
from operator import itemgetter
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import csv

with open('data/processed_tfidf/ALLYEARS/SPARSE1960.dat') as f:
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

logreg = LogisticRegression(C=1e5)
logreg.fit(X,Y)

scores = cross_val_score(logreg, X, Y, cv=5)

print scores.mean()
