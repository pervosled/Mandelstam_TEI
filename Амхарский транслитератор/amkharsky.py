file = open ('amkharsky.tsv', 'r', encoding = 'utf8')

countlines = 0
vocals = []
consonants = []
alphabet = {}
line = []

for line in file:
    countcolumns = 0    
    line = line.strip('\n')
    line = line.split('\t')
    for ch in line:
        ch = ch.strip()
        if countlines == 0 and countcolumns != 0:
            vocals.append(ch)
        if countlines != 0 and countcolumns == 0:
            consonants.append(ch)
        if countlines != 0 and countcolumns != 0:
            alphabet[ch] = consonants[countlines-1]+vocals[countcolumns-1]
        countcolumns+=1
    countlines+=1                     

f1 = open ('Text_1.txt', 'r', encoding = 'utf8')
text = f1.read()
f2 = open ('Text_2.txt', 'w', encoding = 'utf8')

for key, value in alphabet.items():
    text = text.replace(key, value)
f2.write(text)
f1.close()
f2.close()

