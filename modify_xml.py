import lxml.etree as etree
import urllib.request
import os.path
import re
import lxml.html
import csv

pages = []
tnumbers = []

path = '/Users/Alexey/Documents/Python_Projects/Mandelstam_TEI/downloads/'

for file in os.listdir(path):
    if file.endswith('.htm'):
        page = open (path+file, 'r', encoding='cp1251')
        sourcecode = page.read()
        tree = lxml.html.fromstring(sourcecode)

##        номер текущего тома
        volume_n = re.findall('Арт-Бизнес-Центр, 199[0-9]. Т. [1-4]', sourcecode)
##        print(int(volume_n[-1][-1]))

##        номер произведения в томе
        t_number = tree.xpath('.//h1/text()')        
        for element in t_number:
            text_number = re.findall('\d{1,3}\.', element)
            if text_number:
                break
        tnumbers.append(int(text_number[0][:-1]))
##        print(int(text_number[0][:-1]))
##        print(tnumbers[-1]+1)


##        номера страниц
        page = tree.xpath('//div[@class="page"]/text()')
        try: 
            pages.append(int(page[0]))            
        except:
            if tnumbers[-1]==tnumbers[-2]+1:
                pages.append(pages[-1]) 
            else:
                pages.append('')

##        geoindex = open('geohistory_index.csv', 'r', encoding='utf8')
##        rows = csv.reader(geoindex, delimiter='\t')
##        for i in rows:
##            if str(pages[-1])==i[3]:
##                print('yes')
##            else:
##                print('no')

list1 = [['aac','aab','aabbc'],['112','a2m','22221']]
for i in list1:
    if 'aa' in i[1]:
        print('yes')
    else:
        print('no')
 

