import nltk

f = './textdone'
f = open(f,'w')

text = './text'
text = open(text,'r')

for line in text:
	temp = ''
	for c in line:
		if c.isalpha() or c == ' ' or c == '_':
			temp = temp + c
		else:
			temp = temp + ' '
	tokens = nltk.word_tokenize(temp)
	for t in tokens:
		f.write(t+' ')
		#f.write(t.lower()+' ')

f.close()
text.close()
