import lxml.etree as etree
import urllib.request
import os.path
import re
import lxml.html
import csv

path = '/Users/Alexey/Documents/Python_Projects/Mandelstam_TEI/'

## ОТКРЫВАЕМ УКАЗАТЕЛЬ ГЕОГРАФИЧЕСКИХ И ИСТОРИЧЕСКИХ НАЗВАНИЙ И ПАРСИМ ЕГО

vol_page = []
names = []
data = []
vol = []
pg = []
pg1 = []
names_2 = []


with open('myth_index.htm', 'r', encoding='cp1251') as page:
    lines = page.readlines() ## построчный список вида ['str1', 'str2'...]
    for line in lines:

##        вся строка с данными
        line_data = re.findall(r'(<p class="name-ind">.*?</p>)', line)
        if line_data:
            if '&nbsp;' not in line_data:
##                print(line_data) ## например:
## ['<p class="name-ind">Юпитер — <b>II:</b> 251; <b>III:</b> 252 (см. также Зевс)</p>']
                for j in line_data:
                    data.append(j) ## список, внутри строки, 158

##    названия
for a in data:
    name = re.findall(r'name-ind">(.*?) — <b>', a)
    names.append(name) ## список, внутри списки, в каждом по строке с именем или пусто, 158

##    номера томов     
    volumes = re.findall(r'[IV]+', a)
    vol.append(volumes) ## для каждой строки - список, такой: ['IV'],
    ## такой: ['II', 'IV'] или такой: [], 158


## номера страниц
    vol_p = re.split(r'[IV]+', a) ##  часть строки между римскими цифрами
    del vol_p[0]
    pg = [re.findall(r'\d+[;,-]?\d+', element) for element in vol_p]
    pg1.append(pg) ## список, внутри 158 списков по числу статей, внутри один список:
## ['61', '366'], если один том, или больше – по числу томов: [['270'], ['190']]


##    ИТОГ
##print(names[-3])  ## ['Юдифь']
##print(vol[-3])  ## ['I', 'II']
##print(pg1[-3]) ## [['94', '244'], ['482', '573']]

## СОЗДАЁМ CSV-ФАЙЛ С ДАННЫМИ

record_file = open('myth_index.csv', 'w', newline='', encoding='utf8')
writer = csv.writer(record_file, delimiter='\t')
for i in range(len(names)):
    writer.writerow([names[i]]+[vol[i]]+[pg1[i]])
record_file.close()




