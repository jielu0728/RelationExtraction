f = open('./person','r')
res = open('./result','w')

result = []

for line in f:
    phrase = line.split(' ',1)[1]
    if ' ' in phrase:
        temp = phrase.split(' ')[0].split('/')[0]
        for i in range(1,phrase.count(' ')+1):
            temp = temp + ' ' + phrase.split(' ')[i].split('/')[0]
    else:
        temp = phrase.split('/')[0]

    found = 0
    for s in result:
        if s[0] == temp:
            s[1] = s[1] + 1  
            found = 1
    if found == 0:
        result.append([temp,1])

for s in result:
    if s[1] >= 20 and not s[0].isupper():
        res.write(s[0]+'      '+str(s[1])+'\n')

f.close()
res.close()
