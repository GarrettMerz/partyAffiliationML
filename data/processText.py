import io
import unicodedata

text_file = io.open("campaign2012/BO0", "r", encoding="utf-8")
lines = text_file.readlines()

#print lines

for i in range(0, len(lines)):
    lines[i] = unicodedata.normalize('NFKD', lines[i]).encode('ascii','ignore')

print lines

#for i in range(0,100):
 #   print 'reading file %d' % i
  #  with io.open('campaign2012/BO%d' % i, 'r', encoding="utf-8") as myfile:
   #     txt = myfile.read().replace('\n', '')
    #    corpus.append(txt)
