import gensim
import random

model = gensim.models.Word2Vec.load('./model')

f = open('./result_final','r')

res = open('./similarity','w')

#res_2 = open('./not','w')

#seperate all phrases in result
new_res = []

for line in f:
	phrase = line.split('      ')[0]
	if ' ' in phrase:
		for i in range(phrase.count(' ')):
			if phrase.split(' ')[i] not in new_res:
				new_res.append(phrase.split(' ')[i])
	else:
		if phrase not in new_res:
			new_res.append(phrase)

#calculate the similarities between two names
for obj in new_res:
	temp = new_res[:]
	temp.remove(obj)
	for item in temp:
		try:
			s = model.similarity(obj,item)
		except KeyError:
			s = 0
		if s >= 0:
			res.write(obj+'     '+item+'     '+str(s)+'\n')

#find out those who doesn't look like names:
#found = []
#n = 0.0
#for i in range(20):
#	print n/20
#	n = n + 1
#	for obj in new_res:
#		temp = new_res[:]
#		temp.remove(obj)
#		s = 0
#		for i in range(800):
#			l = len(temp)
#			r_1 = random.randint(0,l-1)
#			r_2 = random.randint(0,l-1)
#			r_3 = random.randint(0,l-1)
#			if model.doesnt_match([temp[r_3],temp[r_2],temp[r_1],obj]) == obj:
#				s = s + 1
#		if float(s)/800 > 0.4 and obj not in found:
#			found.append(obj)
#			res_2.write(obj+'\n')


f.close()
res.close()
#res_2.close()