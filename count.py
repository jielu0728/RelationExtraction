f = open('./person','r')

res = open('./result','w')

n = []
for line in f:
	name = line.split('\n')[0]

	found = 0
	for obj in n:
		if obj[0] == name:
			obj[1] = obj[1] + 1
			found = 1
	if found == 0:
		n.append([name,1])

for s in n:
	if s[1] >= 2 and not s[0].isupper():
		res.write(s[0]+'      '+str(s[1])+'\n')

f.close()
res.close()