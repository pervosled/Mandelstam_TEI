import lxml.etree as etree
import urllib.request
import os.path
import re
import lxml.html

path_1 = '/Volumes/Blue Hard/ТЕКСТЫ/Алёша/_ВШЭ/НИС/Мандельштам/2. Конвертируем файлы в TEI/downloads/'
    
path_2 = '/Volumes/Blue Hard/ТЕКСТЫ/Алёша/_ВШЭ/НИС/Мандельштам/2. Конвертируем файлы в TEI/convert/'

##if not os.path.exists(path_2):
##    os.makedirs(path_2)


##ОТКРЫВАЕМ ИСХОДНЫЙ HTML-ФАЙЛ И ПАРСИМ ЕГО ПРИ ПОМОЩИ LXML

for file in os.listdir(path_1):
    if file.endswith('.htm'):
        page = open (path_1+file, 'r', encoding='cp1251')
        sourcecode = page.read()        
        tree = lxml.html.fromstring(sourcecode)
##        заголовок вида 'О.Э. Мандельштам. «Ни о чем не нужно говорить...»'
##        title = tree.xpath('.//title/text()')[0]
##        print(title)        
##        номер произведения в томе (число без точки)
        number = tree.xpath('.//h1/text()')
##        print(int(number[0][:-1]))
##        заголовок, который будет отображаться на странице
        title_view = tree.xpath('.//h1/text()')
##        for i in range(len(title_view)):
##            print(title_view[i])
##        номер текущего тома
        volume = re.findall('Арт-Бизнес-Центр, 199[0-9]. Т. [1-4]', sourcecode)
##        print(int(volume[-1][-1]))        
##        источник публикации (издание, том)
        publication = re.findall('Арт-Бизнес-Центр, 199[0-9]. Т. [1-4]', sourcecode)
##        print(publication[0])
##        номера страниц
        page_number = tree.xpath('.//div[@class="page"]/text()')
##        try:
##            print(int(page_number[0]))
##        except:
##            continue
##        стихотворный размер и количество стоп, если это стихи
        versus = re.findall('<div class="versus[a-z]*[\d]', sourcecode)
##        try:
##            print(versus[0].replace('<div class="versus', ''))
##        except:
##            continue
##        номер строфы, если это стихи
        verse_num = tree.xpath('.//p[@class="stanza"]/@id')
##        print(verse_num)
##        номер строки, если это стихи
        verse_line = tree.xpath('.//span[@class="line"]/@id | .//span[@class="line1r"]/@id')
##        for x in verse_line:
##            print(x[1:])
##        дата (подпись под произведением)
##        date = tree.xpath('.//p[@class="date"]/text()')
##        print(date)
##        собственно текст, если это стихи (строки в виде списка)
        verse_text = tree.xpath('.//span[@class="line"]/text() | .//span[@class="line1r"]/text()')
##        print(verse_text)
##        собственно текст, если это проза или письма (абзацы в виде списка)
        paragraph = tree.xpath('.//p[@class="text"]/text()')
##        print(paragraph)


## СТРОИМ ФАЙЛ TEI XML               

##        xml_file = open(path_2+file[:-4]+'.xml', 'w', encoding = 'utf8')
##        xml_file.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+'<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>'+'\n'+'<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>'+'\n'+'<TEI xmlns="http://www.tei-c.org/ns/1.0">'+'\n')

        teiHeader = etree.Element('teiHeader')
        fileDesc = etree.SubElement(teiHeader, 'fileDesc')
        titleStmt = etree.SubElement(fileDesc, 'titleStmt')        
        title = etree.SubElement(titleStmt, 'title').text = 'О.Э. Мандельштам. Cобрание сочинений в четырёх томах'

        tree = etree.ElementTree(teiHeader)
        tree.write(path_2+file[:-4]+'.xml', encoding = 'utf8', pretty_print = True, xml_declaration=True)

        
 



##<root>
## <doc>
##     <field1 name="blah">some value1</field1>
##     <field2 name="asdfasd">some vlaue2</field2>
## </doc>
##
##</root>
        
        

##  <teiHeader>
##      <fileDesc>
##         <titleStmt>
##            <title>О.Э. Мандельштам. Cобрание сочинений в четырёх томах </title>
##         </titleStmt>
##         <publicationStmt>
##            <p>АРТ-БИЗНЕС-ЦЕНТР МОСКВА 1993</p>
##         </publicationStmt>
##         <sourceDesc>
##            <p>Издание подготовлено Мандельштамовским обществом </p>
##         </sourceDesc>
##      </fileDesc>
##  </teiHeader>

                 

    else:
        continue
    

