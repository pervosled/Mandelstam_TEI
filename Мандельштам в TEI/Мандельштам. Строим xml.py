import lxml.etree as etree
import urllib.request
import os.path
import re
import lxml.html

path_1 = '/Volumes/Blue Hard/ТЕКСТЫ/Алёша/_ВШЭ/НИС/Мандельштам/\
2. Конвертируем файлы в TEI/downloads/'
    
path_2 = \
'/Volumes/Blue Hard/ТЕКСТЫ/Алёша/_ВШЭ/НИС/Мандельштам/\
2. Конвертируем файлы в TEI/convert/'


## ОТКРЫВАЕМ ИСХОДНЫЙ HTML-ФАЙЛ И ПАРСИМ ЕГО ПРИ ПОМОЩИ LXML

for file in os.listdir(path_1):
    if file.endswith('.htm'):
        page = open (path_1+file, 'r', encoding='cp1251')
        sourcecode = page.read()        
        tree = lxml.html.fromstring(sourcecode)
        
##        заголовок вида 'О.Э. Мандельштам. «Ни о чем не нужно говорить...»'
        title = tree.xpath('.//title/text()')[0]
##        print(title)
        
##        номер произведения в томе
        t_number = tree.xpath('.//h1/text()')        
        for element in t_number:
            text_number = re.findall('\d{1,3}\.', element)
            if text_number:
                break
##        print(text_number)
            
##        заголовок, который будет отображаться на странице
        title_view = tree.xpath('.//h1/text()')
##        for i in range(len(title_view)):
##            print(title_view[i])
        
##        номер текущего тома
        volume_n = re.findall('Арт-Бизнес-Центр, 199[0-9]. Т. [1-4]', sourcecode)
##        print(int(volume_n[-1][-1]))
        
##        источник публикации (издание, том)
        publication = re.findall('Арт-Бизнес-Центр, 199[0-9]. Т. [1-4]', sourcecode)
##        print(publication[0])
        
##        номера страниц
        page_number = tree.xpath('.//div[@class="page"]/text()')
##        try:
##            print(int(page_number[0]))
##        except:
##            continue
        
##        тип текста – стихи
        poem = re.findall('<div class="versus[a-z]*[\d]', sourcecode)
##        if poem:
##            print('это стихи')
##        else:
##            print('это не стихи')
        
##        тип текста – письма
        letter = tree.xpath('.//p[@class="ltr-date"]')
##        try:
##            print(letter[0])
##        except:
##            print('это не письма')
        
##        стихотворный размер и количество стоп, если это стихи
        versus = re.findall('<div class="versus[a-z]*[\d]', sourcecode)
        vers = []
        try:
##            print(versus[0].replace('<div class="versus', ''))
            vers.append(versus[0].replace('<div class="versus', ''))
        except:
            continue
##        vers - список с одним элементом вида ['ia6']
        
##        число строф, если это стихи
        verse_num = tree.xpath('.//p[@class="stanza"]/@id')
##        print(verse_num) ## список вида ['st1', 'st2']
##        print(len(verse_num)) ## число строф
        
##        номер строки, если это стихи
##        (список, элементы которого – номера всех строк, например, [1, 2, 3, 4])
        verse_line = tree.xpath('.//span[@class="line"]/@id | .//span[@class="line1r"]/@id')
        linelist = []
        for x in verse_line:
            linelist.append(int(x[1:]))
##        print(linelist)
      
##        сколько строк в стихотворении, если это стихи
##        if verse_line:
##            print(len(verse_line))
        
##        информация о каждой строфе, если это стихи    
        line_list = \
        ['1_line', 'couplet', 'tercet', 'quatrain', 'quintet', 'sestet', 'septet', 'octet', '9_line']
        coup_text = []
        tei_coup_num = []
        len_coup = []
        if poem:
            for x in range(int(verse_num[-1][-1])+1):
                couplet_num = tree.xpath \
                ('//p[@id="st{0}"]//span[@class="line1r"]/@id | \
                //p[@id="st{0}"]//span[@class="line"]/@id'.format(x))

##                информация о каждой строфе: название в TEI (например, quatrain)
                if couplet_num:                    
                    tei_couplet_num = line_list[len(couplet_num)-1]
                    tei_coup_num.append(tei_couplet_num)
##                    tei_coup_num - для одного стихотворения список вида
##                    ['quatrain', 'quatrain', 'quatrain', 'quatrain', 'couplet']

##                    информация о каждой строфе: число строк
##                    print(len(couplet_num)) ## количество строк в строфе, например, 4
                    len_coup.append(len(couplet_num))
##                    len_coup для стихотворения - список чисел, соответствующих
##                    числу строк в каждой строфе, например [4, 4, 4, 4, 2]

##                    информация о каждой строфе: собственно стихи в виде списка                  
                    couplet_text = tree.xpath \
                    ('//p[@id="st{0}"]//span[@class="line"]/text() | \
                    //p[@id="st{0}"]//span[@class="line1r"]/text()'.format(x))
##                    print(couplet_text)                    
                    coup_text.append(couplet_text) 
##                    coup_text - общий список, в который вложены подсписки по числу строф,
##                    элементы каждого подсписка – это отдельные стихи (в виде строк)
                    
##        дата (подпись под произведением)
        date = tree.xpath('.//p[@class="date"]/text()')
##        print(date)
        
##        собственно текст, если это стихи (все строки стихотворения в виде списка)
        verse_text = tree.xpath('.//span[@class="line"]/text() | .//span[@class="line1r"]/text()')
##        print(verse_text)
               
##        собственно текст, если это проза или письма (абзацы в виде списка)
        paragraph = tree.xpath('.//p[@class="text"]/text()')
##        print(paragraph)


## СТРОИМ ФАЙЛ TEI XML               

##        xml_file = open(path_2+file[:-4]+'.xml', 'w', encoding = 'utf8')
##        xml_file.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+ \
##        '<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" \
##        type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>'+'\n'+ \
##        '<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" \
##        type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>'+'\n'+ \
##        '<TEI xmlns="http://www.tei-c.org/ns/1.0">'+'\n')

        tei = etree.Element('TEI', xmlns = "http://www.tei-c.org/ns/1.0")
        teiHeader = etree.SubElement(tei, 'teiHeader')
        fileDesc = etree.SubElement(teiHeader, 'fileDesc')
        titleStmt = etree.SubElement(fileDesc, 'titleStmt')        
        title = etree.SubElement(titleStmt, 'title').text = \
                'О.Э. Мандельштам. Cобрание сочинений в четырёх томах'
        publicationStmt = etree.SubElement(fileDesc, 'publicationStmt')
        p = etree.SubElement(publicationStmt, 'p').text = 'АРТ-БИЗНЕС-ЦЕНТР МОСКВА 1993'        
        sourceDesc = etree.SubElement(fileDesc, 'sourceDesc')
        p = etree.SubElement(sourceDesc, 'p').text = \
            'Издание подготовлено Мандельштамовским обществом'

        text = etree.SubElement(tei, 'text')
        body = etree.SubElement(text, 'body')
        div = etree.SubElement(body, 'div', type = 'volume', n = volume_n[-1][-1])        
        div = etree.SubElement(div, 'div', type = 'part', n = text_number[0][:-1])
        if poem:
            for i in range(len(verse_num)):  ## число строф
                lg = etree.SubElement(div, 'lg', type = '{}'.format(tei_coup_num[i])) ## название, например, sestet
                for s in range(len_coup[i]):  ## число строк в строфе
                    l = etree.SubElement(lg, 'l').text = coup_text[i][s] ## сам текст: стихи
        else:
            continue
                    

##        tree = etree.ElementTree(tei)
##        tree.write(path_2+file[:-4]+'.xml', encoding = 'utf8', pretty_print = True, xml_declaration = True)



            
    else:
        continue
        




