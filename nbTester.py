# EECS 545 HW 2, p3 Naive Bayes
# Rory Fitzpatrick
#
# Estimating probabilities with SPARSE.TRAIN
# p(yi = -1) = 0.500933
# p(yi =  1) = 0.499067
# Testing with SPARSE.TEST
# classification error = 1.62%
#
# tokens most indicative of spam (w, log(p(w|1)/p(w|-1)) ):
# httpaddr (616, 6.60)
# spam (1210, 6.60)
# unsubscrib (1357, 4.99)
# ebai (394, 4.85)
# valet (1369, 5.19)

import numpy as np
from operator import itemgetter

ntokens = 12650

print "Estimating probabilities with train_data.dat"
with open('train_data.dat') as f:
    content = f.readlines()

data = []
for line in content:
   y = int(line.split()[0]) # get spam spam_classification
   wtemp = line.split()[1:] # get word counts

   w = []
   for i in range(0, len(wtemp)):
      w.append((wtemp[i].split(":")[0], wtemp[i].split(":")[1]))
   data.append((y, w))

# calculate p(yi=y) and format data for use
cmat = np.zeros((len(data), ntokens+1)) # matrix indexed by cmat[di-1][wj]
ny1 = 0 # number of elements with y=1

for i in range(0, len(data)):
   if (data[i][0] == 1):
      ny1 += 1
   cmat[i][0] = data[i][0]
   for feat, fval in data[i][1]:
      cmat[i][int(feat)] = int(fval)

py1 = float(ny1)/len(data) # p(y=1)

print "p(yi = -1) = %f" % (1-py1)
print "p(yi =  1) = %f" % (py1)

# this is where we save all p(wj|yi=y) where pwj[0] corresponds to yi=-1
pwj = np.zeros((2,ntokens))

for i in range(0, len(cmat)):
   for j in range(1, len(cmat[0])):
      if cmat[i][0] == 1:
         pwj[1][j-1] += cmat[i][j]
      else:
         pwj[0][j-1] += cmat[i][j]

# Laplace smoothing -- add 1 to all elements
for y in range(0,2):
   for j in range(0, len(pwj[y])):
      pwj[y][j] += 1

denom0 = sum(pwj[0])
denom1 = sum(pwj[1])

indicator = []

for j in range(0, len(pwj[0])):
   pwj[0][j] /= denom0
   pwj[1][j] /= denom1
   indicator.append( ( j+1, np.log(pwj[1][j]/pwj[0][j]) ) )
   # print probabilities if you want them
   # print "p(wj = %d|yi = -1) = %f" % (j+1, pwj[0][j])
   # print "p(wj = %d|yi =  1) = %f" % (j+1, pwj[1][j])

indicator = sorted(indicator, key=itemgetter(1), reverse=True)
print indicator[:5]
indicator = sorted(indicator, key=itemgetter(1))
print indicator[:5]

print "Testing with test_data.dat"
with open('test_data.dat') as f:
    content = f.readlines()

testdata = []

for line in content:
   y = int(line.split()[0]) # get spam spam_classification
   wtemp = line.split()[1:] # get word counts

   w = []
   for i in range(0, len(wtemp)):
      w.append((wtemp[i].split(":")[0], wtemp[i].split(":")[1]))
   testdata.append((y, w))

testcmat = np.zeros((len(testdata), ntokens+1)) # matrix indexed by cmat[di-1][wj]

for i in range(0, len(testdata)):
   if (testdata[i][0] == 1):
      ny1 += 1
   testcmat[i][0] = testdata[i][0]
   for feat, fval in testdata[i][1]:
      testcmat[i][int(feat)] = int(fval)

#calculate p(di|y=1) and p(di|y=-1)
# from here on out I'm working with logs
pdi = np.zeros((2, len(testcmat)))

nwrong = 0

for i in range(0, len(testcmat)):
   for j in range(1,len(testcmat[0])):
      pdi[0][i] += testcmat[i][j]*np.log(pwj[0][j-1])
      pdi[1][i] += testcmat[i][j]*np.log(pwj[1][j-1])

   py1test = (pdi[1][i]*py1) /( pdi[1][i]*py1 + pdi[0][i]*(1-py1) )
   py0test = (pdi[0][i]*(1-py1)) /( pdi[1][i]*py1 + pdi[0][i]*(1-py1) )

   if (py1test < py0test):
      ytest = 1
   else:
      ytest = -1

   if (ytest != testcmat[i][0]):
      nwrong += 1

print "classification error = %0.2f%%" % (float(nwrong)/len(testcmat) * 100)

