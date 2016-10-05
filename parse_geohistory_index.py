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
names_2 = []

with open('geohistory_index.htm', 'r', encoding='cp1251') as page:
    lines = page.readlines() ## построчный список вида ['str1', 'str2'...]
    for line in lines:

##        вся строка с данными
        line_data = re.findall(r'(<p class="name-ind">.*?</p>)', line)
        if line_data:
            if '&nbsp;' not in line_data:
##                print(line_data) ## например: ['<p class="name-ind">Япония — <b>II:</b> 270; <b>III:</b> 190']
                for j in line_data:
                    data.append(j) ## список, внутри строки, 423               

##    названия
for a in data:
    name = re.findall(r'name-ind">(.*?) — <b>', a)
    names.append(name) ## список, внутри списки, в каждом – по строке с именем или пусто, 423
    
##    названия второго порядка
    name_2 = re.findall(r'.*?<br>(.*?) — <b>', a)
    names_2.append(name_2) ## список, внутри списки, в каждом – строки с именами или пусто, 423


    



####    краткие справки
##    description = re.findall(r'</i>(.*?)<b>', a)
##    descr.append(description) ## список, внутри списки, в каждом строка, 1226
##    ## некоторые списки пустые, значит, справки нет (например, перенаправление)
##            
####  остальное
##    vol_p = re.findall(r'<b>(.*)', a)
##    vol_page.append(vol_p)
####print(vol_page)  ## список, внутри списки: ['III:</b> 136, 156—158'; III: 370], 1226
##    ## некоторые списки пустые (например, перенаправление)
##
####  тома
##for i in vol_page:
##    if i:
##        volumes = re.findall(r'[IV]+', i[0])
##    else:
##        volumes = [''] ## для каждой строки - список, такой: ['IV'],
##        ## такой: ['II', 'IV'] или такой: [''], 1226
##    vol.append(volumes)
##
####  страницы
##for i in vol_page:
##    if i:
##        pages = re.split(r'[IV]+', i[0])
##    else:
##        pages = ['']
##    pg.append(pages) ## список, подсписки: ['', ':</b> 294; <b>', ':</b> 112'], 1226
##pg = [[st.replace('<b>','') for st in sublist] for sublist in pg]
##pg = [[st.replace('</b>','') for st in sublist] for sublist in pg]
##pg = [[st.replace(';','') for st in sublist] for sublist in pg]
##pg = [[st.replace(':','') for st in sublist] for sublist in pg]
##pg = [[st.replace(' ','') for st in sublist] for sublist in pg]
##for sublist in pg:
##    if '' in sublist:
##        sublist.remove('')
####print(pg) ## список, подсписки: ['459—461,639', '370', '198,402,416'], 1226
##
####    ИТОГ
####print(names[-891])  ## Яхонтов, Владимир Николаевич
####print(descr[-891])  ## [' (1899—1945), актер — ']
####print(vol[-891])  ## ['II', 'III', 'IV']
####print(pg[-891]) ## ['459—461,639', '370', '198,402,416']
##
#### СОЗДАЁМ CSV-ФАЙЛ С ДАННЫМИ
##
##record_file = open('name_index.csv', 'w', newline='', encoding='utf8')
##writer = csv.writer(record_file, delimiter='\t')
##for i in range(len(names)):
##    writer.writerow([names[i]]+[descr[i]]+[vol[i]]+[pg[i]])
##record_file.close()




