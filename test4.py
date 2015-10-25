import gensim

model = gensim.models.Word2Vec.load('./model')

f = open('./result_final','r')

res = open('./most_similar','w')

person = []

for line in f:
	name = line.split('      ')[0]
	if ' ' in name:
		for obj in name.split(' '):
			if obj not in person:
				person.append(obj)
	else:
		if name not in person:
			person.append(name)

num = 0
for obj1 in person:
	print float(num)/float(len(person))
	num = num + 1
	for obj2 in person:
		for obj3 in person:
			if obj1 != obj2 and obj2 != obj3 and obj3 != obj1:
				temp = []
				value = []
				result = model.most_similar(positive=[obj1,obj2], negative=[obj3], topn=20)
				for c in result:
					if c[0] in person:
						temp.append(c[0])
						value.append(c[1])
				if len(temp) != 0:
					res.write(obj1+' to '+obj3+' =  ?  to  '+obj2+'     ')
					for i in range(len(temp)):
						res.write(temp[i]+' '+str(value[i])+'  ')
					res.write('\n')

f.close()
res.close()