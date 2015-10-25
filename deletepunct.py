import string

f = open('./text','r')
res = open('./text_without_punct', 'w')


for line in f:
	line = "".join(l for l in line if l not in string.punctuation)
	res.write(line)

f.close()
res.close()