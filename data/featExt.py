from nltk.corpus import stopwords, names
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
import io, unicodedata, re

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

corpus = []

for i in range(0,105):
    with io.open('campaign2012/BO%d' % i, 'r') as myfile:
        txt = myfile.read().replace('\n', ' ')
        txt = ''.join([i if ord(i) < 128 else ' ' for i in txt])
        txt = unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore')
        txt = re.sub("\d+", " ", txt)
        txt = re.sub("-", " ", txt)
        txt = re.sub("'", " ", txt)
        txt = re.sub("\.", " ", txt)
        corpus.append(txt)

for i in range(0,101):
    with io.open('campaign2012/MR%d' % i, 'r') as myfile:
        txt = myfile.read().replace('\n', ' ')
        txt = ''.join([i if ord(i) < 128 else ' ' for i in txt])
        txt = unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore')
        txt = re.sub("\d+", " ", txt)
        txt = re.sub("'", " ", txt)
        txt = re.sub("\.", " ", txt)
        txt = re.sub("-", " ", txt)
        corpus.append(txt)

vectorizer = CountVectorizer(stop_words=s, tokenizer=LemmaTokenizer())
X = vectorizer.fit_transform(corpus)
all_tokens = vectorizer.get_feature_names()

print all_tokens
print len(all_tokens)
