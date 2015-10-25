f = open('./result','r')

res = open('./change','w')

line_len = []
for line in f:
	if len(line_len) == 0:
		line_len.append(len(line))
	else:
		line_len.append((len(line)+line_len[-1]))
f.seek(0)

n = 0
for line in f:
	n = n + 1
	name = line.split('      ')[0]
	if ' ' in name:
		found = 0
		for obj in name.split(' '):
			f.seek(0)
			num = 0
			for l in f:
				num = num + 1
				if obj+' ' in l and num != n:
					found = 1
		f.seek(line_len[n-1])
		if found == 0:
			temp = name.replace(' ','_')
			res.write(name+'      '+temp+'\n')


f.close()
res.close()