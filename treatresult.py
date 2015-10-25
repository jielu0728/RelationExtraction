f = open('./result','r')

f_2 = open('./not','r')

res = open('./result_new','w')

deleted = open('./deleted','w')

delete_line = []
for line in f_2:
	word = line.split('\n')[0]
	n = 0
	for l in f:
		if (word+' ') in l:
			deleted.write(l)
			delete_line.append(n)
		n = n + 1
	f.seek(0)

n = 0
for line in f:
	if n not in delete_line:
		res.write(line)
	n = n + 1

f.close()
f_2.close()
res.close()
deleted.close()