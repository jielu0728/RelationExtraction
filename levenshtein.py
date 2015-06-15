f = open('result','r')
res = open('distance','w')

name = []

for line in f:
    name.append(line.split('      ')[0])

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
 
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
 
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]

for obj1 in name:
    for obj2 in name:
        if obj1 != obj2:
            res.write(obj1+'     '+obj2+'     '+str(levenshtein(obj1,obj2))+'\n')

f.close()
res.close()