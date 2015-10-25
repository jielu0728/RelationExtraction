import nltk

f = open('./text','r')

res = open('./text_related','w')

for line in f:
	#line = line.decode('utf-8')
	tokens = nltk.word_tokenize(line)
	tagged = nltk.pos_tag(tokens)
	sentence = nltk.ne_chunk(tagged, binary = False)
	for c in sentence:
		res.write(str(c)+'\n')


f.close()
res.close()