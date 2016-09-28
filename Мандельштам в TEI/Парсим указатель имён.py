import lxml.etree as etree
import urllib.request
import os.path
import re
import lxml.html

path = '/Volumes/Blue Hard/ТЕКСТЫ/Алёша/_ВШЭ/НИС/Мандельштам/\
2. Конвертируем файлы в TEI/Указатель имён/'

## ОТКРЫВАЕМ УКАЗАТЕЛЬ ИМЁН И ПАРСИМ ЕГО ПРИ ПОМОЩИ LXML

vol_page = []
names = []
descr = []
data = []
vol = []
pg = []
for file in os.listdir(path):
    if file.endswith('.htm'):
        page = open (path+file, 'r', encoding='cp1251')   
        lines = page.readlines() ## построчный список вида ['str1', 'str2'...]
        for line in lines:

##            вся строка с данными
            line_data = re.findall(r'<p class="name-ind">(.*?)</p>', line)
##        print(line_data) ## например: ['<i>Шушлетин</i> — <b>III:</b> 437']
            for j in line_data:
                data.append(j) ## список, внутри строки, 1226
                
##    имена
for a in data:
    name = re.findall(r'<i>(.*?)</i>', a)
    names.append(name[0]) ## список, элементы которого – строки - имена, 1226

##    краткие справки
    description = re.findall(r'</i>(.*?)<b>', a)
    descr.append(description) ## список, внутри списки, в каждом строка, 1226
    ## некоторые списки пустые, значит, справки нет (например, перенаправление)
            
##  остальное
    vol_p = re.findall(r'<b>(.*)', a)
    vol_page.append(vol_p)
##print(vol_page)  ## список, внутри списки: ['III:</b> 136, 156—158'; III: 370], 1226
    ## некоторые списки пустые (например, перенаправление)

##  тома
for i in vol_page:
    if i:
        volumes = re.findall(r'[IV]+', i[0])
    else:
        volumes = [''] ## для каждой строки - список, такой: ['IV'],
        ## такой: ['II', 'IV'] или такой: [''], 1226
    vol.append(volumes)

##  страницы
for i in vol_page:
    if i:
        pages = re.split(r'[IV]+', i[0])
    else:
        pages = ['']
    pg.append(pages) ## список, подсписки: ['', ':</b> 294; <b>', ':</b> 112'], 1226
pg = [[st.replace('<b>','') for st in sublist] for sublist in pg]
pg = [[st.replace('</b>','') for st in sublist] for sublist in pg]
pg = [[st.replace(';','') for st in sublist] for sublist in pg]
pg = [[st.replace(':','') for st in sublist] for sublist in pg]
pg = [[st.replace(' ','') for st in sublist] for sublist in pg]
for sublist in pg:
    if '' in sublist:
        sublist.remove('')
##print(pg) ## список, подсписки: ['459—461,639', '370', '198,402,416'], 1226

##    ИТОГ
##print(names[-2])  ## Яхонтов, Владимир Николаевич
##print(descr[-2])  ## [' (1899—1945), актер — ']
##print(vol[-2])  ## ['II', 'III', 'IV']
##print(pg[-2]) ## ['459—461,639', '370', '198,402,416']



