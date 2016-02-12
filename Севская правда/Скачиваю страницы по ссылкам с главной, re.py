import urllib.request
import re
import os.path

openpage=urllib.request.urlopen('http://pravda-sevsk.ru/')
mainpage=openpage.read().decode('cp1251')
sourcecode = open ('list.txt', 'w', encoding = 'utf8')
sourcecode.write(mainpage)
sourcecode.close()

sourcecode=open('list.txt', 'r', encoding = 'utf8')
linklist=open('linklist.txt', 'w', encoding = 'utf8')
pattern = 'a href="http://pravda-sevsk.ru+[\S]+html'
links = re.findall (pattern, mainpage)
links = str(links)
linklist.write (links)
linklist.close()


linklist=open('linklist.txt', 'r', encoding = 'utf8')
linklist2=open('linklist2.txt', 'w', encoding = 'utf8')
text = linklist.read()
text = str(text)
text = text.replace("a href=", '\n')
text = text.replace(",", "")
text = text.replace("[", "")
text = text.replace("]", "")
text = text.replace("'", "")
text = text.replace('"', '')

linklist2.write(text)
linklist2.close()

links = open('LinkList2.txt', 'r')
for link in links:
    link = link.strip()
    name = link.rsplit('/', 1)[-1]
    filename = os.path.join('downloads', name)

    if not os.path.isfile(filename):
        print('Downloading: ' + filename)
        try:
            urllib.request.urlretrieve(link, filename)
        except Exception as inst:
            print(inst)
            print('  Encountered unknown error. Continuing.')
