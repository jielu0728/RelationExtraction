import nltk
import ner
tagger = ner.SocketNER(host='localhost', port=8080)

f = open('./text','r')

res = open('./person','w')

for line in f:
	#tokens = nltk.word_tokenize(line)
	#tagged = nltk.pos_tag(tokens)
	#sentence = nltk.ne_chunk(tagged, binary = False)
	#for c in sentence:
	#	if 'PERSON' in str(c):
	#		res.write(str(c)+'\n')
	if 'PERSON' in tagger.get_entities(line):
		for i in range(len(tagger.get_entities(line)['PERSON'])):
			res.write(tagger.get_entities(line)['PERSON'][i]+'\n')

f.close()
res.close()
