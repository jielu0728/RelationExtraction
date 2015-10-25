import nltk
import string
import jsonrpclib
import json
from nltk.corpus import wordnet as wn
from simplejson import loads
import re
from string import punctuation
server = jsonrpclib.Server("http://localhost:8080")
r = re.compile(r'[{}]'.format(punctuation))




f = open('annotation_speaker')
n = 0
instance = []
temp = []
speaker = []
p = 0
keyposition = []   #the linenum of the paragraph to be treated
for line in f:
    if n <= 38000:
        if '###############' in line:
            keyposition.append(p)
            current = [temp.pop()]
            previous = temp[:]
            temp = []
            continue
        if 'speaker:	' in line:
            speaker.append(line.split('speaker:	')[1].split('\r\n')[0])
            instance.append([current,previous,temp])
            temp = []
            p = 0
            continue
        if line.replace(' ','') != '\r\n':
            temp.append(line.replace('\r\n',''))
            p = p+1
    n = n+1
with open('./result_parser.json', 'w') as fp:
	s = 0
	for i in range(len(instance)):
		print 'progress : '+ str(float(s)/len(instance)*100) +'%\n'
		fp.write('#######seperator instance\n')
		for j in range(3):
			fp.write('#######seperator cases\n')
			for k in range(len(instance[i][j])):
				fp.write('########seperator paragraphs\n')
				result = loads(server.parse(instance[i][j][k]))
				json.dump(result,fp)
				fp.write('\n')
		s = s+1


f.close()
fp.close()