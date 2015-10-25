f = open('./target_text')

n = 0
counter = 0
for line in f:
	if line.replace('\r\n','') == '':
		counter += 1
	else:
		counter = 0
	if counter > 2:
		print n
	n += 1

f.close()