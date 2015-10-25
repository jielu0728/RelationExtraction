from random import randint
f = open('./text','r')

res = open('./target_text','w')

temp = []

counter = 0
for i in range(0,30):
	line = f.readline()
	temp.append(line)

for line in f:
	t = temp.pop(0)
	if t.replace(' ','') != '\r\n' and t != '\r\n':
		counter += 1 
	temp.append(line)
	if '"' in temp[18]:
		c = 0
		for i in range(len(temp)):
			if i < 18:
				res.write(temp[i])
				if temp[i].replace(' ','') != '\r\n' and temp[i] != '\r\n':
					c += 1
			elif i > 18:
				res.write(temp[i])
			else:
				res.write(temp[i]+'###############'+str(counter+c))
		res.write('\nspeaker:	\n\n\n')

f.close()
res.close()