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

text = []
f = open('./text')

for line in f:
    if line.replace(' ','') != '\r\n':
        text.append(line)

with open('./result_parser_target_new.json', 'w') as fp:
    n = 0
    for obj in text:
        temp = obj.strip('\r\n')
        print 'process : '+str(float(n)/len(text))+'\n'
    	fp.write('########seperator\n')
    	result = loads(server.parse(temp))
    	json.dump(result,fp)
    	fp.write('\n')
        n += 1


f.close()
fp.close()