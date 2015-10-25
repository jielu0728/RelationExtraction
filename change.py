f = open('./result','r')

res = open('./change','w')

for line in f:
	name = line.split('      ')[0]
	if ' ' in name:
		res.write(name+'      '+name.replace(' ','_')+'\n')

f.close()
res.close()