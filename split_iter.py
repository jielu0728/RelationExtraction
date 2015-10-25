from nltk.tag.stanford import POSTagger
import string
import os

english_postagger = POSTagger('./stanford-postagger-2015-04-20/models/english-bidirectional-distsim.tagger', './stanford-postagger-2015-04-20/stanford-postagger.jar')

location = './AGameOfThrones/'

def remove_punct(line):
    temp = ''
    for c in line:
        if c == '\'':
            temp = temp + ' ' + c
        elif c not in string.punctuation:
            temp = temp + c
        else:
            temp = temp + ' '
    return temp


for subdir, dirs, files in os.walk(location):
	for f in files:
		res = open(location+'tokens/'+f,'w')
		f = open(location+f,'r')
		for line in f:
			temp = remove_punct(line)
			tokens = english_postagger.tag(temp.split())
			for obj in tokens[0]:
				res.write('('+obj[0]+','+obj[1]+')'+' ')
			res.write('\n')

		f.close()
		res.close()


