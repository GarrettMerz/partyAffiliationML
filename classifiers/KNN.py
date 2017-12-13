import numpy as np
import scipy.io as sio
from collections import Counter

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

train_year = '1960'
test_year = '1960'

tokens_size = file_len('../data/processed_wf/'+train_year+'/TOKEN_LIST')
train_images = np.zeros((file_len('../data/processed_wf/'+train_year+'/train_data.dat'), tokens_size))
test_images = np.zeros((file_len('../data/processed_wf/'+test_year+'/test_data.dat'), tokens_size))
train_labels = np.zeros(file_len('../data/processed_wf/'+train_year+'/train_data.dat'))
test_labels = np.zeros(file_len('../data/processed_wf/'+test_year+'/test_data.dat'))

with open('../data/processed_wf/'+train_year+'/train_data.dat') as f:
#get labels, calculate frequency sums
 for i, line in enumerate(f):
  label = line.split('  ')[0]
  train_labels[i] = int(label)
  text = line.split('  ')[1]
  for cell in text.strip().split(' '):
   word, freq = cell.split(':')
   train_images[i,int(word)-1] = int(freq)

with open('../data/processed_wf/'+test_year+'/test_data.dat') as g:
#get labels, calculate frequency sums
 for i, line in enumerate(g):
  label = line.split('  ')[0]
  test_labels[i] = int(label)
  text = line.split('  ')[1]
  for cell in text.strip().split(' '):
   word, freq = cell.split(':')
   test_images[i,int(word)-1] = int(freq)

#print(train_images)
#print(test_labels.shape)

#train_images = np.asarray(train_data[:,1:785])
#train_labels = np.asarray(train_data[:,0])
#test_images = np.asarray(test_data[:,1:785])
#test_labels = np.asarray(test_data[:,0])

klist = [1, 10, 25, 40]
for k in klist:
 errorcount = 0
 for i in range(test_labels.size):
  test_image = test_images[i]
  test_label = test_labels[i]
  distances = [(np.linalg.norm((test_image - image), 1), label) for (image, label) in zip(train_images, train_labels)]
  distsort = sorted(distances, key = lambda tup: tup[0])
  k_labels = [label for (_, label) in distsort[0:k]]
  win_label, freq = Counter(k_labels).most_common()[0]
  if (int(win_label) != int(test_label)):
   errorcount += 1
 print('for k =', end = ' ')
 print(k, end = ' ')
 print('the error is ', end = ' ')
 print(errorcount/test_labels.size)
