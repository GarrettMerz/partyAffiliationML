from nltk.corpus import stopwords, names
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
import io, unicodedata, re
import numpy as np

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
        self.ps = PorterStemmer()
    def __call__(self, doc):
        temp = [self.wnl.lemmatize(t) for t in word_tokenize(doc)]
        return [self.ps.stem(t) for t in temp]

s1 = set(stopwords.words('english'))
s2 = set(names.words('male.txt'))
s3 = set(names.words('female.txt'))
s = s1 | s2 | s3
s = {x.lower() for x in s}

s.add('{')
s.add('!')
s.add('$')
s.add("'")
s.add("''")
s.add("'d")
s.add("'ll")
s.add("'m")
s.add("'re")
s.add("'s")
s.add("'splainin")
s.add("'ve")
s.add('(')
s.add(')')
s.add(',')
s.add('.')
s.add('/')
s.add(':')
s.add('?')
s.add(';')
s.add('[')
s.add(']')
s.add('%')
s.add('&')
s.add('``')
s.add('#')

corpus = []
party = []

with io.open('allfiles2008.list', 'r') as filelist:
    allfiles = filelist.readlines()

for thisfile in allfiles:
    if "/R/" in str(thisfile):
        party.append(-1)
    else:
        party.append(1)
    with io.open(str(thisfile).strip(), 'r') as myfile:
        txt = myfile.read().replace('\n', ' ')
        txt = ''.join([i if ord(i) < 128 else ' ' for i in txt])
        # txt = unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore')
        txt = re.sub("\d+", " ", txt)
        txt = re.sub("-", " ", txt)
        txt = re.sub("'", " ", txt)
        txt = re.sub("\.", " ", txt)
        corpus.append(txt)

# print party

vectorizer = CountVectorizer(stop_words=s, tokenizer=LemmaTokenizer(), max_features=5000)
X = vectorizer.fit_transform(corpus)
all_tokens = vectorizer.get_feature_names()

# print all_tokens
# print X.toarray()

Y = X.toarray()

N = len(Y)
nt = np.zeros(len(Y[0]))

for i in range(0, len(Y)):
    for j in range(0, len(Y[i])):
        if Y[i][j] != 0:
            nt[j] += 1

print N
print nt

outfile = open("outfile.dat", "w")

for i in range(0, len(Y)):
    thisline = '' + str(party[i]) + ' '
    for j in range(0, len(Y[i])):
        if Y[i][j] != 0:
            thisweight = Y[i][j] * np.log(1 + float(N)/nt[j])
            thisline += str(j+1) + ':' + str(thisweight) + ' '
    thisline += '\n'
    outfile.write(thisline)

outfile.close()

token_list = open("TOKEN_LIST", "w")

for i in range(0, len(all_tokens)):
    thisline = '' + str(i+1) + ' ' + all_tokens[i] + '\n'
    token_list.write(thisline)

# print all_tokens
# print len(all_tokens)