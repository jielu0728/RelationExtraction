f = open('./text','r')

rep = open('./change','r')

res = open('./text_new','w')

replacement = []
for line in rep:
	replacement.append((line.split('      ')[0], line.split('      ')[1].split('\n')[0]))

for line in f:
	for obj in replacement:
		line = line.replace(obj[0], obj[1])
	res.write(line)

f.close()
rep.close()
res.close()