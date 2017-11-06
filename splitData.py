with open('outfile.dat') as f:
    content = f.readlines()

i = 0

train_data = open("train_data.dat", "w")
test_data = open("test_data.dat", "w")

i = 0
for thisline in content:
   i += 1
   if (i%5 == 0):
      test_data.write(thisline)
   else:
      train_data.write(thisline)