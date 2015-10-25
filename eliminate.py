f = open('./feature_chapiter','r')

res = open('./result','r')

res_new = open('./result_new','w')

MIN_CHAPITERS = 10

feature = [] 

name = []
for line in res:
	name.append(line.split('      ')[0])

for line in f:
    temp = map(float, line.replace('[','').replace(']','').split(',')[:])
    feature.append(temp)

count = [sum(x) for x in feature]
eliminated = []
for i in range(len(count)):
	if count[i] <= MIN_CHAPITERS:
		eliminated.append(i)

for j in range(len(name)):
	if j not in eliminated:
		res_new.write(name[j]+'      \n')


f.close()
res.close()
res_new.close()