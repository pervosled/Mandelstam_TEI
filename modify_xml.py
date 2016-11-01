import lxml.etree as etree
import urllib.request
import os.path
import re
import lxml.html

path = '/Users/Alexey/Documents/Python_Projects/Mandelstam_TEI/convert/'


## ОТКРЫВАЕМ ИСХОДНЫЙ HTML-ФАЙЛ И ПАРСИМ ЕГО ПРИ ПОМОЩИ LXML

for file in os.listdir(path):
    page = open (path+file, 'r')
    sourcecode = page.read()        
    tree = lxml.html.fromstring(sourcecode)



## если в колонке vol то же, что в div n, если в соответствующей её колонке
## pg1 то же, что и в  
