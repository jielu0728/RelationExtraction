import os
import string

location = './AGameOfThrones'
f = open('./result', 'r')

res = open('./feature_chapiter','w')

name = []
chapiter = []
for line in f:
	name.append(line.split('      ')[0])
	chapiter.append([])

f.close()

# distinguish those prefixes and suffixes
similar = []
for obj_1 in name:
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
def distinguish(temp, name, chapiter, line, n):
	is_substring = 0
	treated = line
	for obj in temp:
		treated = treated.replace(obj,'')
	if name+' ' not in treated:
		is_substring = 1
	if is_substring == 0:
		chapiter[n].append(1)
	return is_substring
		

for subdir, dirs, files in os.walk(location):
	for f in files:
		text = open('./AGameOfThrones/'+f,'r')
		n = 0      
		for obj in name:
			found = 0
			temp = []
			find_fullname(temp,obj)
			for line in text:
				line = "".join(l for l in line if l not in string.punctuation)
				if distinguish(temp, obj, chapiter, line, n) == 0:
					found = 1
					break
			if found == 0:
				chapiter[n].append(0)
			n = n + 1
			text.seek(0)
		text.close()


for obj in chapiter:
	res.write('[')
	n = 0
	for unit in obj:
		n = n + 1
		if n != len(obj):
			res.write(str(unit)+',')
		if n == len(obj):
			res.write(str(unit)+']\n')

res.close()