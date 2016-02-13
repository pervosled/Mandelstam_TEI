import urllib.request
import os.path
import lxml.html
import re

links = []

openpage = urllib.request.urlopen('http://pravda-sevsk.ru/')
mainpage = openpage.read().decode('cp1251')
tree = lxml.html.fromstring(mainpage)

def AddLink(tree):       
    for url in tree.xpath('//a/@href'):
        if 'http' not in url:
            url = 'http://pravda-sevsk.ru' + url  
            if url not in links: 
                links.append(url)
        if url not in links and 'pravda-sevsk' in url:
            links.append(url)
            
AddLink(tree)

for link in links:
    try:
        response = urllib.request.urlopen(link)
        page = response.read().decode('cp1251')
        tree = lxml.html.fromstring(page)
        for url in tree.xpath('//a/@href'):
            if 'http' or 'https' not in url:
                url = 'http://pravda-sevsk.ru' + url  
                if url not in links: 
                    links.append(url)
        if url not in links and 'pravda-sevsk' in url:
            links.append(url)            
    except:
        continue



file = open('Alllinks.txt', 'w', encoding = 'utf8')
for i, line in enumerate(links):
    file.write(line + '\n')
file.close()
