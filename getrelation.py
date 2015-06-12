import json

f = open('./text','r')
f_no_punct = open('./text_without_punct', 'r')
person = open('./result','r')

res = open('./relation','w')

ft = open('./feature','w')

name = []
feature = []
for line in person:
	name.append(line.split('      ')[0])

# distinguish those prefixes and suffixes
times_total = {}
similar = []
for obj_1 in name:
	times_total[obj_1] = 0
	feature.append([])
	similar.append([obj_1])
	found = 0
	for obj_2 in name:
		if obj_1 != obj_2 and ' ' in obj_2:
			if obj_1 in obj_2.split(' '):
				similar[-1].append(obj_2)
				found = 1
	if found == 0:
		similar.pop()

def find_fullname(temp, name):
	for obj in similar:
		if name in obj:
			for c in obj:
				if c != name and name in c:
					temp.append(c)


# not to mix up those prefixes or suffixes with full names
def distinguish(temp, name, found, line, n):
	is_substring = 0
	treated = line
	for obj in temp:
		treated = treated.replace(obj,'')
	if name+' ' not in treated:
		is_substring = 1
	if is_substring == 0:
		found.append(n)

MAX_LINE = 2
already_treated = []
iteration = 0             # X vector
name_line = {}

# find all apparences of names
for obj in name:
	name_line[obj] = []
	n = 0
	temp = []            # possible full names
	find_fullname(temp, obj)
	for line in f_no_punct:
		n = n + 1
		distinguish(temp, obj, name_line[obj], line, n)
	f_no_punct.seek(0)

print 'lists created'

for name_1 in name:
	print 'progress: '+str(float(iteration)/len(name)*100)
	num_2 = 0
	for name_2 in name:
		if name_1 == name_2:
			feature[iteration].append(-1)
			already_treated.append((name_1,name_2))
		if name_2 != name_1 and (name_1,name_2) not in already_treated:
			res.write('relation:  '+name_1+'    and    '+name_2+'  |  '+name_2+'    and    '+name_1+'   :\n')
			times = 0
			for obj1 in name_line[name_1]:
				for obj2 in name_line[name_2]:
					if abs(obj1-obj2) <= MAX_LINE:
						times = times + 1
						res.write(str(times)+'  :\n')
						n = 0
						for line in f:
							n = n + 1
							if n >= min(obj1,obj2) and n <= max(obj1,obj2):
								res.write(line)
						f.seek(0)
			times_total[name_1] = times_total[name_1] + times
			times_total[name_2] = times_total[name_2] + times
			feature[iteration].append(times)
			feature[num_2].append(times)
			res.write('\n\nnumber total found : '+str(times)+'\n\n\n')
			already_treated.append((name_1,name_2))
			already_treated.append((name_2,name_1))
		num_2 = num_2 + 1
	iteration = iteration + 1
		

with open('./record.json', 'w') as fp:
	json.dump(times_total, fp ,indent = 4, sort_keys = True)

for obj in feature:
	ft.write('[')
	n = 0
	for unit in obj:
		n = n + 1
		if n != len(obj):
			ft.write(str(unit)+',')
		if n == len(obj):
			ft.write(str(unit)+']\n')

f.close()
person.close()
res.close()
ft.close()
f_no_punct.close()