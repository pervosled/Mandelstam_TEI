import urllib.request
import os.path
import lxml.html
import re

links = []

name = "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko"
try:
    openpage = urllib.request.Request('http://pravda-sevsk.ru/', headers = {'User-Agent': name})
    openpage = urllib.request.urlopen('http://pravda-sevsk.ru/')
    mainpage = openpage.read().decode('cp1251')
    tree = lxml.html.fromstring(mainpage)
except urllib.error.HTTPError as err:
    print(err.code)

def AddLink(tree):       
    for url in tree.xpath('//a/@href'):
        if url not in links and 'http' not in url:
            url = 'http://pravda-sevsk.ru' + url        
            links.append(url)
        if url not in links and 'pravda-sevsk' in url:
            links.append(url)
            
AddLink(tree)

for link in links:
    try:
        response = urllib.request.Request(link, headers = {'User-Agent': name})
        response = urllib.request.urlopen(link)
        page = response.read().decode('cp1251')
        tree = lxml.html.fromstring(page)
    except urllib.error.HTTPError as err:
        print(err.code)
    AddLink(tree)

file = open('Untitled.txt', 'w', encoding = 'utf8')
for i, line in enumerate(links):
    file.write(line)
file.close()

