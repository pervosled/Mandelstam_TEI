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


with open('geohistory_index.htm', 'r', encoding='cp1251') as page:
    lines = page.readlines() ## построчный список вида ['str1', 'str2'...]
    for line in lines:

##        вся строка с данными
        line_data = re.findall(r'(<p class="name-ind">.*?</p>)', line)
        if line_data:
            if '&nbsp;' not in line_data:
##                print(line_data) ## например:
                ## ['<p class="name-ind">Япония — <b>II:</b> 270; <b>III:</b> 190']
                for j in line_data:
                    data.append(j) ## список, внутри строки, 423               

##    названия
for a in data:
    name = re.findall(r'name-ind">(.*?) — <b>', a)
    names.append(name) ## список, внутри списки, в каждом по строке с именем или пусто, 423
    
##    названия второго порядка
    name_2 = re.findall(r'.*?<br>(.*?) — <b>', a)
    names_2.append(name_2) ## список, внутри списки, в каждом строки с именами или пусто, 423

##    номера томов     
    volumes = re.findall(r'[IV]+', a)
    vol.append(volumes) ## для каждой строки - список, такой: ['IV'],
    ## такой: ['II', 'IV'] или такой: [], 423

## номера страниц
    vol_p = re.split(r'[IV]+', a) ##  часть строки между римскими цифрами
    del vol_p[0]
    pg = [re.findall(r'\d+[;,-]?\d+', element) for element in vol_p]
    pg1.append(pg)
##print(pg1) ## список, внутри 423 списка по числу статей, внутри один список: ['61', '366'],
## если один том, или больше – по числу томов: [['270'], ['190']]


##    ИТОГ
##print(names[-34])  ## ['Царское (Детское) Село (г. Пушкин)']
##print(names_2[-34])  ## [' Китайская деревня']
##print(vol[-34])  ## ['I', 'II', 'IV', 'IV']
##print(pg1[-34]) ## [['76', '239'], ['485'],
## ['13', '44', '53', '61', '62', '72', '77', '78', '81', '82', '84-88', '92', '93', '95'],
## ['53', '83', '84', '88']]

## СОЗДАЁМ CSV-ФАЙЛ С ДАННЫМИ

record_file = open('geohistory_index.csv', 'w', newline='', encoding='utf8')
writer = csv.writer(record_file, delimiter='\t')
for i in range(len(names)):
    writer.writerow([names[i]]+[names_2[i]]+[vol[i]]+[pg1[i]])
record_file.close()




