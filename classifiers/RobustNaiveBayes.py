import numpy as np
import heapq

numspam = 0
numgood = 0
guessgoodfiles = 0
guessbadfiles = 0
robust_spam_count = 0
robust_good_count = 0
tokens_size = 12650
linenum = 0
probwordgivspam, probwordgivgood, spamsum, goodsum, logprobs = [0]*tokens_size, [0]*tokens_size, [0]*tokens_size, [0]*tokens_size, [0]*tokens_size

with open('../data/processed_wf/2016/train_data.dat') as f:
#get labels, calculate frequency sums
 for i, line in enumerate(f):
  label = line.split('  ')[0]
  text = line.split('  ')[1]
  for cell in text.strip().split(' '):
   word, freq = cell.split(':')
   if int(label) == 1:
    spamsum[int(word)-1] += int(freq)
    numspam += 1
   if int(label) == -1:
    goodsum[int(word)-1] += int(freq)
    numgood += 1

 #get probability of good & spam
probspam = numspam / (numspam + numgood)
probgood = numgood / (numspam + numgood)

#Remove Laplace Smoothing! Check tokens to see which ones aren't in train set
#for i in range(0, tokens_size):
 #if spamsum[i] == 0 && goodsum[i] == 0:
  #robust_spam_count += 1
 #if goodsum[i] == 0:
  #robust_good_count += 1


#use frequency sums to get conditionals
for i in range(0, tokens_size):
  probwordgivspam[i] = (spamsum[i])/(sum(spamsum))
  probwordgivgood[i] = (goodsum[i])/(sum(goodsum))

# logprobs[i] = np.log(probwordgivspam[i]/probwordgivgood[i])

numdocs = 0
misclass = 0

print("Number of tokens not in train set of R speeches is") 
print(robust_spam_count)
print("Number of tokens not in train set of D speeches is") 
print(robust_good_count)

#get labels
with open('../data/processed_wf/2016/test_data.dat') as g:
 for i, line in enumerate(g):
  linenum += 1
  numdocs += 1
  guesslabel = 0
  logpost = np.log(probspam/probgood)
  words_not_in_train_good = 0
  words_not_in_train_spam = 0
  testwords = []
  testlabel = line.split('  ')[0]
  testtext = line.split('  ')[1]
  for cell in testtext.strip().split(' '):
   testword, testfreq = cell.split(':')
   testwords.append(int(testword)-1)
  for test in testwords:
   if (probwordgivspam[test] == 0) && (probwordgivgood[test] == 0):
    if (probwordgivspam[test] == 0):
     words_not_in_train_good += 1
    if (probwordgivgood[test] == 0):
     words_not_in_train_spam += 1

 else logpost += np.log(probwordgivspam[test]/probwordgivgood[test])
  if (logpost > 0):
   guesslabel = 1
   guessgoodfiles += 1
  elif (logpost < 0):
   guesslabel = -1
   guessbadfiles += 1
  #if (int(testlabel) == guesslabel):
   #print(int(testlabel))
  if (int(testlabel) != guesslabel):
   misclass += 1
   print(linenum)

error = float((misclass/numdocs)*100.0)

#print("error is")
#print(error)
#print("republican speeches number guess is")
#print(guessbadfiles)
#print("democrat speeches number guess is")
#print(guessgoodfiles)

#print("Democratic-est words are at")
#Democraticest = heapq.nlargest(5, range(len(logprobs)), logprobs.__getitem__)
#print(Democraticest + np.ones(len(Democraticest)))

#print("Republican-est words are at")
#Republicanest = heapq.nsmallest(5, range(len(logprobs)), logprobs.__getitem__)
#print(Republicanest + np.ones(len(Republicanest)))


