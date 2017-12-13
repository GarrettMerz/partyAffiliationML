import numpy as np
import heapq

tokens_size = 10801 # 1960
# tokens_size = 11252 # 2008
# tokens_size = 6951 # 2016
probwordgivR, probwordgivD, Rsum, Dsum, logprobs = [0]*tokens_size, [0]*tokens_size, [0]*tokens_size, [0]*tokens_size, [0]*tokens_size

with open('data/processed_wf/1960/SPARSE.dat') as f:
   #get labels, calculate frequency sums
   for i, line in enumerate(f):
      label = line.split('  ')[0]
      text = line.split('  ')[1]
      # print i
      for cell in text.strip().split(' '):
         word, freq = cell.split(':')
         if int(label) == 1:
            Rsum[int(word)-1] += float(freq)
         if int(label) == -1:
            Dsum[int(word)-1] += float(freq)

 #use frequency sums to get conditionals
for i in range(0, tokens_size):
   probwordgivR[i] = (1 + Rsum[i])/(len(Rsum)+sum(Rsum))
   probwordgivD[i] = (1 + Dsum[i])/(len(Dsum)+sum(Dsum))
   logprobs[i] = np.log(probwordgivR[i]/probwordgivD[i])

republican = heapq.nlargest(5, range(len(logprobs)), logprobs.__getitem__)
print(republican + np.ones(len(republican)))

democrat = heapq.nsmallest(5, range(len(logprobs)), logprobs.__getitem__)
print(democrat + np.ones(len(democrat)))