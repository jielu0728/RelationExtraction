
# coding: utf-8

# In[1]:

import nltk
import string
import jsonrpclib
from simplejson import loads
import simplejson
from nltk.corpus import wordnet as wn
import re
from string import punctuation

server = jsonrpclib.Server("http://localhost:8080")
r = re.compile(r'[{}]'.format(punctuation))


# name appears in the paragraph before
# 
# 
# 2 alternant lines 
# 
# if the name appears in the previous or following utterance with a pattern such as ',name,'
# 
# the object of the speech verb
# 

# In[2]:

f = open('annotation_speaker')
res = open('./candidate.data','w')
n = 0
instance = []
temp = []
speaker = []
p = 0
keyposition = []   #the linenum of the paragraph to be treated
for line in f:
    if n <= 30420:
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
#print instance[-1]


#instance [0,1,2]:
#0 : current paragraph (including the object utterance)
#1 : 9 previous paragraphs
#2 : 5 following paragraphs


# In[3]:

result = loads(server.parse(instance[0][1][7]))
#print result['sentences'][0]['parsetree'].split('] [')


# In[4]:

def countwordperline(instance,num_instance):
    numlist = []
    for i in range(3):
        for j in range(len(instance[num_instance][i])):
            new_strs = r.sub(' ',instance[num_instance][i][j])
            num = len(new_strs.split())
            numlist.append(num)
    numlist.insert(keyposition[num_instance]-1, numlist.pop(0))
    return numlist
            
#countwordperline(instance,0)


# In[5]:

def convertoffset(numlist,linenum,offset,sentence):
    temp = sentence[0:offset]
    new_strs = r.sub(' ',temp)
    num = len(new_strs.split())
    pos = 0
    for i in range(linenum-1):
        try:
            pos = pos + numlist[i]
        except IndexError:
            print numlist,linenum,offset,sentence
            cccccccccccccccccccccc
    return pos+num+1

#convertoffset(countwordperline(instance,0),keyposition[0],33,instance[0][0][0])


# In[6]:

# no use, we can get the index from the loop number
def convertposition(numlist,linenum,position): 
    temp = position
    i = 0 
    while temp > 0:
        temp = temp - numlist[i]
        i = i+1
    i = i-1
    if i == linenum-1:
        return 0,0
    elif i>linenum-1:
        return 2,i-linenum
    else:
        return 1,i

#convertposition(countwordperline(instance,0),keyposition[0],669)


# In[7]:

def ner(instance):
    entities = []
    n = 0
    for obj in instance:
        numlist = countwordperline(instance,n)
        print 'progress : '+str(float(n)/float(len(instance))*100)+'%\n'
        current = [[]]
        temp = []
        for z in range(len(loads(server.parse(obj[0][0]))['sentences'])):
            temp = temp + loads(server.parse(obj[0][0]))['sentences'][z]['parsetree'].split('] [')
        for frag in temp:
            if 'PartOfSpeech=NNP' in frag:
                text = frag.split('Text=')[1].split(' ')[0]
                position = frag.split('CharacterOffsetBegin=')[1].split(' ')[0]
                pos = convertoffset(numlist,keyposition[n],int(position),obj[0][0])
                current[0].append([text,int(position),pos])
            elif 'PartOfSpeech=N' in frag:
                text = frag.split('Text=')[1].split(' ')[0]
                position = frag.split('CharacterOffsetBegin=')[1].split(' ')[0]
                pos = convertoffset(numlist,keyposition[n],int(position),obj[0][0])
                lex = []
                for synset in wn.synsets(text):
                    lex.append(synset.lexname())
                if lex == []:
                    continue
                elif float(lex.count('noun.person'))/float(len(lex)) >= 0.4:
                    current[0].append([text,int(position),pos])
        word = loads(server.parse(obj[0][0]))['sentences'][0]['words'][0]
        if word[1]['PartOfSpeech'] == 'NNP':
            text = word[0]
            position = word[1]['CharacterOffsetBegin']
            pos = convertoffset(numlist,keyposition[n],int(position),obj[0][0])
            current[0].append([text,int(position),pos])
        elif 'N' in word[1]['PartOfSpeech']:
            text = word[0]
            position = word[1]['CharacterOffsetBegin']
            pos = convertoffset(numlist,keyposition[n],int(position),obj[0][0])
            lex = []
            for synset in wn.synsets(text):
                lex.append(synset.lexname())
            if lex == []:
                pass
            elif float(lex.count('noun.person'))/float(len(lex)) >= 0.4:
                current[0].append([text,int(position),pos])
        previous = []
        for i in range(len(obj[1])):
            previous.append([])
            temp = []
            for x in range(len(loads(server.parse(obj[1][i]))['sentences'])):
                try:
                    temp = temp + loads(server.parse(obj[1][i]))['sentences'][x]['parsetree'].split('] [')
                    temp = temp + loads(server.parse(obj[1][i]))['sentences'][x]['words'][0]
                except IndexError:
                    continue
            for frag in temp:
                if 'PartOfSpeech=NNP' in frag:
                    text = frag.split('Text=')[1].split(' ')[0]
                    position = frag.split('CharacterOffsetBegin=')[1].split(' ')[0]
                    pos = convertoffset(numlist,i+1,int(position),obj[1][i])
                    previous[i].append([text,int(position),pos])
                elif 'PartOfSpeech=N' in frag:
                    text = frag.split('Text=')[1].split(' ')[0]
                    position = frag.split('CharacterOffsetBegin=')[1].split(' ')[0]
                    pos = convertoffset(numlist,i+1,int(position),obj[1][i])
                    lex = []
                    for synset in wn.synsets(text):
                        lex.append(synset.lexname())
                    if lex == []:
                        continue
                    elif float(lex.count('noun.person'))/float(len(lex)) >= 0.4:
                        previous[i].append([text,int(position),pos])
            word = loads(server.parse(obj[1][i]))['sentences'][0]['words'][0]
            if word[1]['PartOfSpeech'] == 'NNP':
                text = word[0]
                position = word[1]['CharacterOffsetBegin']
                pos = convertoffset(numlist,i+1,int(position),obj[1][i])
                previous[i].append([text,int(position),pos])
            elif 'N' in word[1]['PartOfSpeech']:
                text = word[0]
                position = word[1]['CharacterOffsetBegin']
                pos = convertoffset(numlist,i+1,int(position),obj[1][i])
                lex = []
                for synset in wn.synsets(text):
                    lex.append(synset.lexname())
                if lex == []:
                    pass
                elif float(lex.count('noun.person'))/float(len(lex)) >= 0.4:
                    previous[i].append([text,int(position),pos])
        following = []
        for j in range(len(obj[2])):
            following.append([])
            temp = []
            for y in range(len(loads(server.parse(obj[2][j]))['sentences'])):
                try:
                    temp = temp + loads(server.parse(obj[2][j]))['sentences'][y]['words'][0]
                    temp = temp + loads(server.parse(obj[2][j]))['sentences'][y]['parsetree'].split('] [')
                except IndexError:
                    continue
            for frag in temp:
                if 'PartOfSpeech=NNP' in frag:
                    text = frag.split('Text=')[1].split(' ')[0]
                    position = frag.split('CharacterOffsetBegin=')[1].split(' ')[0]
                    pos = convertoffset(numlist,keyposition[n]+j+1,int(position),obj[2][j])
                    following[j].append([text,int(position),pos])
                elif 'PartOfSpeech=N' in frag:
                    text = frag.split('Text=')[1].split(' ')[0]
                    position = frag.split('CharacterOffsetBegin=')[1].split(' ')[0]
                    pos = convertoffset(numlist,keyposition[n]+j+1,int(position),obj[2][j])
                    lex = []
                    for synset in wn.synsets(text):
                        lex.append(synset.lexname())
                    if lex == []:
                        continue
                    if float(lex.count('noun.person'))/float(len(lex)) >= 0.4:
                        following[j].append([text,int(position),pos])
            if word[1]['PartOfSpeech'] == 'NNP':
                text = word[0]
                position = word[1]['CharacterOffsetBegin']
                pos = convertoffset(numlist,keyposition[n]+j+1,int(position),obj[2][j])
                following[j].append([text,int(position),pos])
            elif 'N' in word[1]['PartOfSpeech']:
                text = word[0]
                position = word[1]['CharacterOffsetBegin']
                pos = convertoffset(numlist,keyposition[n]+j+1,int(position),obj[2][j])
                lex = []
                for synset in wn.synsets(text):
                    lex.append(synset.lexname())
                if lex == []:
                    pass
                elif float(lex.count('noun.person'))/float(len(lex)) >= 0.4:
                    following[j].append([text,int(position),pos])
        entities.append([current,previous,following])
        n = n +1
    return entities

entities = ner(instance)
entities_new = entities[:]
#print entities

#entities [name, offset in the paragraph, word position in the instance]


# In[8]:

#combine contiguous name entities and separate those within and outside quotation marks
def contiguous(instance,namelist,ni,cls,nl):
    i = 0
    t = len(namelist)-1
    newlist = {}
    newlist['in'] = []
    newlist['out'] = []
    while i < t:
        if namelist[i+1][1]-namelist[i][1] == len(namelist[i][0])+1 and instance[ni][cls][nl][namelist[i][1]+len(namelist[i][0])] == ' ':
            namelist[i][0] = namelist[i][0]+' '+namelist[i+1][0]
            namelist.pop(i+1)
            t = t - 1
            i = i - 1
        i = i + 1
    for obj in namelist:
        if instance[ni][cls][nl][0:obj[1]].count('"')%2 == 1:
            newlist['in'].append(obj)
        else:
            newlist['out'].append(obj)
    return newlist

for i in range(len(entities)):
    for j in range(3):
        for k in range(len(instance[i][j])):
            entities_new[i][j][k] = contiguous(instance,entities[i][j][k],i,j,k)


simplejson.dump(entities_new, res)
res.close()

