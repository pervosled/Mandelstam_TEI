import lxml.etree as etree
import urllib.request
import os.path
import re
import lxml.html

path_1 = '/Users/Alexey/Documents/Python_Projects/Mandelstam_TEI/downloads_all/'

path_2 = '/Users/Alexey/Documents/Python_Projects/Mandelstam_TEI/convert_all/'


## ОТКРЫВАЕМ ИСХОДНЫЙ HTML-ФАЙЛ И ПАРСИМ ЕГО ПРИ ПОМОЩИ LXML

for file in os.listdir(path_1):
    if file.endswith('.htm'):
        page = open (path_1+file, 'r', encoding='cp1251')
        sourcecode = page.read()        
        tree = lxml.html.fromstring(sourcecode)


##Общие свойства
        
##        заголовок вида 'О.Э. Мандельштам. «Ни о чем не нужно говорить...»'
        title = tree.xpath('.//title/text()')[0]
##        print(title)

##        заголовок вида '«Ни о чем не нужно говорить...»'
        short_title = title.replace('О.Э. Мандельштам. ', '')
##        print(short_title)
        
##        номер произведения в томе
        t_number = tree.xpath('.//h1/text()')        
        for element in t_number:
            text_number = re.findall('\d{1,3}\а?.', element)
            if text_number:
                break
##        print(text_number)
            
##        заголовок, который будет отображаться на странице
        title_list = []
        title_count = tree.xpath('count(.//h1)') 
##        print(int(title_count)) ## число заголовочных тегов <h1>       
        for t in range(int(title_count)):
            title_view = tree.xpath('.//h1[{0}]/text()'.format(t+1))
##            print(title_view)
            title_list.append(title_view)
##        print(title_list) ## список, внутри которого подсписки
        ## по числу пар тегов <h1></h1> в файле, например:
        ## [['ПРОЗА', '\n1921—1929'], ['177.', '\nБАТУМ']]
                  
##        номер текущего тома
        volume_n = re.findall('Арт-Бизнес-Центр, 199[0-9]. Т. [1-4]', sourcecode)
##        print(int(volume_n[-1][-1]))
        
##        источник публикации (издание, том)
        publication = re.findall('Арт-Бизнес-Центр, 199[0-9]. Т. [1-4]', sourcecode)
##        print(publication[0])
                           
##        дата (подпись под произведением)
        date = tree.xpath('.//p[@class="date"]/text()')
##        print(date)
        if date:
            year = re.findall('19\d{2}', date[0]) ## список, внутри строка (строки) с годом
            year_exact = re.findall('19\d{2}(?!\?|\(\?)', date[0]) ## список,
            ## внутри строка (строки) с годом, если после не идёт '?' или '(?)'
            year_proposed = re.findall('19\d{2}\?|19\d{2}\(\?\)', date[0])
##            print(year_proposed) ## список,
            ## внутри строка (строки) с годом, если после идёт '?' или '(?)'
##            full_date = re.findall('.*?\d{1,2}.*?(янв|фев|мар|апр|ма|июн|июл|авг|сент|окт|ноя|дек).*?', date[0])
            full_date = re.findall('^.*?\d\d(янв|фев|мар|апр|ма|июн|июл|авг|сент|окт|ноя|дек)(0[1-9]|[1-2][0-9]|3[01])$', date[0])             
##            print(full_date)
            

##        номера страниц
        page = tree.xpath('//div[@class="page"]/text()')
##        print(page)
##        try:
##            print(int(page[0]))
##        except:
##            print('no page number')

##        посвящение
        dedication = tree.xpath('//div[@class="dedication"]//text() | //p[@class="dedication"]//text()')
##        print(dedication)

##        эпиграф
        epigraph = tree.xpath('//p[@class="epigr"]//text() | //div[@class="epigr"]//text()')
##        print(epigraph)

##        автор эпиграфа
        epigraph_src = tree.xpath('//p[@class="source"]//text()')
##         print(epigraph_src)

##        сноска
        note = tree.xpath('//div[@class="footnote"]//text()')
##        print(note)
        
       

##Стихи
        
##        тип текста – стихи
        poem = re.findall('<div class="versus', sourcecode)
        poem_1 = re.findall('<p class="versus', sourcecode)
        if poem_1:
            poem = 'versus'
##        if poem:
##            print('это стихи')
##        else:
##            print('это не стихи')
        if poem:
            genre = 'poem'

##        стихотворный размер и количество стоп, если это стихи
        versus = re.findall('<div class="versus[a-z]*[\d]', sourcecode)
        vers = []
##        try:
##            print(versus[0].replace('<div class="versus', ''))
##            vers.append(versus[0].replace('<div class="versus', ''))
##        except:
##            continue
##        vers - список с одним элементом вида ['ia6']
      
##        число строф, если это стихи
        verse_num = tree.xpath('.//p[@class="stanza"]/@id')
        if poem:
            if not verse_num:
                verse_num = ['st1']
##        print(verse_num) ## список вида ['st1', 'st2']
##        print(len(verse_num)) ## число строф
        
##        номер строки, если это стихи
##        (список, элементы которого – номера всех строк, например, [1, 2, 3, 4])
        verse_line = tree.xpath('.//span[@class]/@id')
        linelist = []
        for x in verse_line:
            linelist.append(int(x[1:]))
##        print(linelist)
      
##        сколько строк в стихотворении, если это стихи
##        if verse_line:
##            print(len(verse_line))
##        if poem:
##            print(linelist[-1]) ## это и есть число строк, например, 16
##        else:
##            print('not poem')
       
##        информация о каждой строфе, если это стихи    
        line_list = \
        ['1_line', 'couplet', 'tercet', 'quatrain', 'quintet', 'sestet', 'septet', 'octet']
        coup_text = []
        tei_coup_num = []
        len_coup = []

##        if poem:
##            print(len(verse_num)) ## число строф, если это стихи
        
        if poem:
            for x in range(len(verse_num)):
                couplet_num = tree.xpath('//p[@id="st{0}"]//span/@id'.format(x+1))
##                print(couplet_num) ## для каждой строфы – список вида ['L1', 'L2', 'L3', 'L4']
                if not couplet_num:
                    couplet_num = tree.xpath('//div[@class]//span[@class]/@id')
##                print(couplet_num) ## для всего стихотворения список вида ['L1', 'L2', 'L3', 'L4']
                
##                информация о каждой строфе: название в TEI (например, quatrain)
                try:
                    tei_couplet_num = line_list[len(couplet_num)-1]
                except IndexError:
                    tei_couplet_num = str(len(couplet_num))+'_line'
                tei_coup_num.append(tei_couplet_num)
##            print(tei_coup_num) ## tei_coup_num - для одного стихотворения список вида
                    ## ['quatrain', 'quatrain', 'quatrain', 'quatrain', 'couplet']

##                    информация о каждой строфе: число строк
##                    print(len(couplet_num)) ## количество строк в строфе, например, 4
                len_coup.append(len(couplet_num)) 
##            print(len_coup) ## len_coup для стихотворения - список чисел, соответствующих
                ## числу строк в каждой строфе, например [4, 4, 4, 4, 2] OK
##
##                    информация о каждой строфе: собственно стихи в виде списка                  
                if int(verse_num[-1][-1])>1:
                    couplet_text = tree.xpath \
                    ('//p[@id="st{0}"]//span[@class]/text()'.format(x+1))
                else:
                    couplet_text = tree.xpath('//span[@class]/text()')
##                    print(couplet_text)                    
                coup_text.append(couplet_text)
##            print(coup_text) ## coup_text - общий список, в который вложены подсписки по числу строф,
                    ## элементы каждого подсписка – это отдельные стихи (в виде строк)
                           
##        собственно текст, если это стихи (все строки стихотворения в виде списка)
        verse_text = tree.xpath('.//span[@class="line"]/text() | .//span[@class="line1r"]/text()')
##        print(verse_text)
        
##        текст последней стихотворной строчки перед разрывом страницы
        poemlasttxt = []
        if poem:
            plasttxt = tree.xpath('.//div[@class="page"]/preceding::span[1]/text()')
            for n in plasttxt:
                poemlasttxt.append(n)
##            print(poemlasttxt)## списки соответствуют файлам, вложенные
            ## в них строки - это абзацы, предшествующие разрыву страниц

##Письма
        
##        тип текста – письма
        letter = tree.xpath('.//p[@class="ltr-date"]')
##        try:
##            print(letter[0])
##        except:
##            print('это не письма')
        if letter:
            genre = 'letter'

##        текст последней нестихотворной строки перед разрывом страницы
        if not poem:
            plasttxt = tree.xpath('.//div[@class="page"]/preceding::p[1]/text()')
##            print(plasttxt) ## список, элементы которого - строки -
            ## это абзацы, предшествующие разрыву страниц

##Пьеса

##        тип текста - пьеса
        drama = tree.xpath('.//p[@class="remark"] | .//p[@class="speaker"] | \
.//p[@class="speaker"] | .//p[@class="stage"]')
        if drama:
            genre = 'play'
        if poem and drama:
            genre = 'play in verse'

##Проза
               
##        собственно текст, если это проза или письма (каждый абзац - строка, \
##                все вместе в одном списке, если не проза или письма, выдаёт пустой список)
        paragraph = tree.xpath('.//p[@class="text"]/text() | .//p[@class="text-cont"]/text()')
##        print(paragraph)
##        тип текста - проза
        if paragraph and not letter and not drama:
            genre = 'prose'
            

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
        profileDesc = etree.SubElement(teiHeader, 'profileDesc')
        textDesc = etree.SubElement(profileDesc, 'textDesc', n = genre)
        titleStmt = etree.SubElement(fileDesc, 'titleStmt')        
        title = etree.SubElement(titleStmt, 'title').text = short_title
        author = etree.SubElement(titleStmt, 'author').text = 'О.Э. Мандельштам'
        publicationStmt = etree.SubElement(fileDesc, 'publicationStmt')
        p = etree.SubElement(publicationStmt, 'p').text = 'АРТ-БИЗНЕС-ЦЕНТР МОСКВА 1993'        
        sourceDesc = etree.SubElement(fileDesc, 'sourceDesc')
        p = etree.SubElement(sourceDesc, 'p').text = \
            'Издание подготовлено Мандельштамовским обществом'

        text = etree.SubElement(tei, 'text')
        body = etree.SubElement(text, 'body')
        div1 = etree.SubElement(body, 'div1', type = 'volume', n = volume_n[-1][-1])        
        try:
            div2 = etree.SubElement(div1, 'div2', type = 'part', n = text_number[0][:-1])
        except IndexError:
            div2 = etree.SubElement(div1, 'div2', type = 'part', n = '')        

        for head in title_list:
##            print(''.join(head))
            head = etree.SubElement(div2, 'head').text = ''.join(head) ## заголовок

        if dedication: ## посвящение
            dedic = etree.SubElement(div2, 'div', type = 'dedication').text = ''.join(dedication)

        if epigraph: ## эпиграф
            epig = etree.SubElement(div2, 'epigraph')

        if epigraph: ## эпиграф
            epig_quot = etree.SubElement(epig, 'quote').text = ''.join(epigraph)

        if epigraph_src: ## эпиграф: автор
            epi_src = etree.SubElement(epig, 'bibl').text = ''.join(epigraph_src)
            
        if poem:
            k = 0
            c = 0
            for i in range(len(verse_num)):  ## число строф
                lg = etree.SubElement(div2, 'lg', type = '{}'.format(tei_coup_num[i])) \
                     ## название, например, sestet
                for s in range(len_coup[i]):  ## число строк в строфе
                    l = etree.SubElement(lg, 'l', n = str(linelist[k])).text = coup_text[i][s] \
                    ## сам текст: стихи
                    k += 1
##                    if poemlasttxt:
##                        for t in poemlasttxt:
##                            if coup_text[i][s]==t:
##                                pb = etree.SubElement(div2, 'pb').text = page[c] ## номера страниц
##                            else:
##                                continue
##                            c += 1                    
        if not poem:
            c = 0
            for m in range(len(paragraph)):
                p1 = etree.SubElement(div2, 'p').text = paragraph[m] ## проза: текст
##                for z in plasttxt:
##                    if paragraph[m] == z:
##                        pb = etree.SubElement(div2, 'pb').text = page[c] ## номера страниц
##                        ## в нужном месте (проза, письма)
##                    else:
##                        continue
##                    c += 1
        
        if date:
            if year:
                if year_proposed:
                    dateline = etree.SubElement(div2, 'date', when = '#'.join(year) \
                                            , precision = "circa").text = date[0]
                else:
                    dateline = etree.SubElement(div2, 'date', when = '#'.join(year)).text = date[0]
##            if year_exact: ## точный год
##                dateline = etree.SubElement(div2, 'date', when = ', '.join(year_exact)).text = date[0]
                           

                

        if note:
            nte = etree.SubElement(div2, 'note').text = ''.join(note) ## ссылка
                                               
        tree = etree.ElementTree(tei)
        tree.write(path_2+file[:-4]+'.xml', encoding = 'utf8', pretty_print = True, \
                   xml_declaration = True)
        

