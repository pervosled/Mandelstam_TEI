import urllib.request
import os.path
import lxml.html

def AddLink(links):
    for url in tree.xpath('//a/@href'):
        if url.startswith('/'):
            url = 'http://pravda-sevsk.ru' + url  
            if url not in links: 
                links.append(url)
                print(url)
            else:
                continue                
        else:
            if url not in links and 'pravda-sevsk' in url:
                links.append(url)            
                print(url)
            else:
                continue
    return links

links = []
openpage = urllib.request.urlopen('http://pravda-sevsk.ru/')
mainpage = openpage.read().decode('cp1251')
tree = lxml.html.fromstring(mainpage)
            
AddLink(links)

for link in links:
    try:
        response = urllib.request.urlopen(link)
        page = response.read().decode('cp1251')
        tree = lxml.html.fromstring(page)
        AddLink(links)               
    except:
        continue
