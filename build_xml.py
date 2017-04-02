import lxml.etree as etree
import urllib.request
import os.path
import re
import lxml.html
import csv
import signal

path_1 = '/Users/Alexey/Documents/Python_Projects/Mandelstam_TEI/downloads_all/'

path_2 = '/Users/Alexey/Documents/Python_Projects/Mandelstam_TEI/convert_all/'


## ОТКРЫВАЕМ ИСХОДНЫЙ HTML-ФАЙЛ И ПАРСИМ ЕГО ПРИ ПОМОЩИ LXML

page_n_1 = []
g_page_n_1 = []

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

##        авторский текст (только само произведение и теги рядом)
        auth_text = re.search('Версия: конец(.*?)Копирайт: начало', sourcecode, re.DOTALL)
        auth_text = auth_text.group().split('\n')
        
##        номер произведения в томе
        for a in range(9):
            t_number = tree.xpath('.//h{0}/text()'.format(a+1))
        
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
        volume_n = re.findall('Арт-Бизнес-Центр, 199[0-9]. Т. [1-4]', \
                              sourcecode)
##        print(int(volume_n[-1][-1]))
        vols = {1:'I', 2:'II', 3:'III', 4:'IV'}
        volume_n_roman = (vols[(int(volume_n[-1][-1]))])
##        print(volume_n_roman) ## номер тома римскими цифрами, напр.: 'II'
        
        
##        источник публикации (издание, том)
        publication = re.findall('Арт-Бизнес-Центр, 199[0-9]. Т. [1-4]', \
                                 sourcecode)
##        print(publication[0])
                           
##        дата (подпись под произведением)
        full_date_when = []
        full_date_from = {}
        full_date_to = {}
        full_date = []
        years = []
        days = []
        worm_mark = []

        date = tree.xpath('.//p[@class="date"]/text()')
##        print(date)  ## например: ['1912 (1913?), 2 января 1937']
        if date:
##            print(date)
            year_split = re.findall(r'(.*?19\d{2}.*?[,—]?)', date[0])
##            print(year_split) ## превратили '17—18 марта 1931, конец 1935'
            ## в ['17—18 марта 1931,', ' конец 1935']           
            for u in year_split:
                year = re.findall('19\d{2}', u) ## год, например: ['1908']
                full_d = {}
                months = []                
                full_d['y'] = year
##                not_after = re.findall('поздн', u)
##                if not_after:
##                    for z in not_after:
##                        full_d.append(not_after)                
                month = re.findall \
('.*?(нва|евр|арт|прел|мая|май|Ма|июн|Июн|июл|Июл|авг|Авг|ент|окт|Окт|ояб|дек|Дек).*?', u)
                month_dict = {'нва':'01', 'евр':'02', 'арт':'03', \
                'прел':'04', 'мая':'05', 'май': '05', 'Ма':'05', 'июн':'06', 'Июн':'06', 'июл':'07', \
                'Июл':'07', 'авг':'08', 'Авг':'08', 'ент':'09', 'окт':'10', 'Окт':'10', \
                              'ояб':'11', 'дек':'12', 'Дек':'12'}
                if month:
                    for e in month:
                        months.append(month_dict[e])
                    full_d['m'] = months ## номера месяцев в отдельном списке внутри списка full_d
                day = re.sub('\d{4}', '', u) ## удаляем четырёхзначные числа (годы)
                day = re.findall('\d{1,2}', day) ## ищем только числа (дни)                
                if day:
                    for n,i in enumerate(day):
                        if len(i) == 1:
                            day[n] = '0'+i
                    full_d['d'] = day              
                full_date.append(full_d)
##            print(full_date) ## [{'d': ['24'], 'y': ['1911'], 'm': ['11']}, {'y': ['1915']}]
                ## – т.е. 24 ноября 1911, 1915(?)
            if len(year_split) == 2:
                for y in year_split:
                    if 'позднее' in y:
                        full_date_to['m'] = full_date[0]['m'][0]
                        full_date_to['d'] = full_date[0]['d'][0]
                        full_date_to['y'] = full_date[0]['y'][0]
                    worm_end = re.search(r'[—-]\s?$', y) ## тире в конце y
                    worm_start = re.search(r'^\s?[—-]', y) ## тире в начале y
                    if worm_end or worm_start:
                        worm_mark.append('a')
                        full_date_from = full_date[0]
                        full_date_to = full_date[1]
##                        print(date[0]) ## 8 декабря 1936 — 17 января 1937
##                        print(full_date_from) ## {'y': ['1936'], 'm': ['12'], 'd': ['8']}
##                        print(full_date_to) ## {'y': ['1937'], 'm': ['01'], 'd': ['17']}
                    if not worm_end and not worm_start:
                        if '—' in y or '-' in y:
                            try:
                                if len(full_date[0]['m']) == 2:
                                    full_date_from['y'] = full_date[0]['y'][0]
                                    full_date_from['m'] = full_date[0]['m'][0]
                                    full_date_to['m'] = full_date[0]['m'][1]
                                    full_date_to['y'] = full_date[0]['y'][0]
                                if len(full_date[0]['d']) == 2:
                                    full_date_from['y'] = full_date[0]['y'][0]
                                    full_date_from['m'] = full_date[0]['m'][0]
                                    full_date_from['d'] = full_date[0]['d'][0]
                                    full_date_to['m'] = full_date[0]['m'][0]
                                    full_date_to['d'] = full_date[0]['d'][1]
                                    full_date_to['y'] = full_date[0]['y'][0]
                            except:
                                continue
            if len(year_split) == 1:
                if 'позднее' in year_split[0]:
                    try:
                        full_date_to['m'] = full_date[0]['m'][0]
                        full_date_to['d'] = full_date[0]['d'][0]
                        full_date_to['y'] = full_date[0]['y'][0]
                    except:
                        continue
                if '—' in year_split[0] or '-' in year_split[0]:
                    if '-го' not in year_split[0]:
                        try:
                            if len(full_date[0]['d']) == 2 and len(full_date[0]['m']) == 2:
                                full_date_from['d'] = full_date[0]['d'][0]
                                full_date_from['y'] = full_date[0]['y'][0]
                                full_date_from['m'] = full_date[0]['m'][0]
                                full_date_to['d'] = full_date[0]['d'][1]
                                full_date_to['m'] = full_date[0]['m'][1]
                                full_date_to['y'] = full_date[0]['y'][0]
                            if len(full_date[0]['d']) == 2 and len(full_date[0]['m']) == 1:
                                full_date_from['d'] = full_date[0]['d'][0]
                                full_date_from['y'] = full_date[0]['y'][0]
                                full_date_from['m'] = full_date[0]['m'][0]
                                full_date_to['d'] = full_date[0]['d'][1]
                                full_date_to['m'] = full_date[0]['m'][0]
                                full_date_to['y'] = full_date[0]['y'][0]
                            if len(full_date[0]['d']) == 1 and len(full_date[0]['m']) == 2:
                                worm_dig = re.search(r'—\s?\d', year_split[0])
                                if worm_dig:
                                    full_date_from['y'] = full_date[0]['y'][0]
                                    full_date_from['m'] = full_date[0]['m'][0]
                                    full_date_to['d'] = full_date[0]['d'][0]
                                    full_date_to['m'] = full_date[0]['m'][1]
                                    full_date_to['y'] = full_date[0]['y'][0]
                                else:
                                    full_date_from['d'] = full_date[0]['d'][0]
                                    full_date_from['y'] = full_date[0]['y'][0]
                                    full_date_from['m'] = full_date[0]['m'][0]
                                    full_date_to['m'] = full_date[0]['m'][1]
                                    full_date_to['y'] = full_date[0]['y'][0]
                        except:
                            continue
##            print(date[0]) ## Февраль — 14 мая 1932
##            print(full_date)
##            print(full_date_from) ## {'y': '1932', 'm': '02'}
##            print(full_date_to) ## {'d': '14', 'm': '05', 'y': '1932'}
        
##        номера страниц
        page_n = tree.xpath('//div[@class="page"]/text()')
        if page_n:
            page_n_1.append(page_n[-1])
##        print(page_n_1) ## если нет номера страницы, оставляем его же из предыдущего файла: ['84']
##        print(page_n) ## например: ['84']
##        try:
##            print(int(page_n[0])) ## например: 84
##        except:
##            print('no page number')

##        посвящение
        dedication = tree.xpath('//div[@class="dedication"]//text() | \
//p[@class="dedication"]//text()')
##        print(dedication)

##        эпиграф
        epigraph = tree.xpath('//p[@class="epigr"]//text() | \
//div[@class="epigr"]//text()')
##        print(epigraph)

##        автор эпиграфа
        epigraph_src = tree.xpath('//p[@class="source"]//text()')
##         print(epigraph_src)

##        сноска
        note = tree.xpath('//div[@class="footnote"]//text()')
##        print(note)
        

## Мифологические герои

        path = '/Users/Alexey/Documents/Python_Projects/Mandelstam_TEI/'
        
        vol_page = []
        names = []
        data = []
        vol = []
        pg = []
        pg1 = []
        names_2 = []
        myth_names = []
        myth_names1 = []


        with open('myth_index.htm', 'r', encoding='cp1251') as page:
            lines = page.readlines() ## построчный список вида ['str1', 'str2'...]
            for line in lines:

        ##        вся строка с данными
                line_data = re.findall(r'(<p class="name-ind">.*?</p>)', line)
                if line_data:
                    if '&nbsp;' not in line_data:
        ##                print(line_data) ## например:
        ## ['<p class="name-ind">Юпитер — <b>II:</b> 251; <b>III:</b> 252 (см. также Зевс)</p>']
                        for j in line_data:
                            data.append(j) ## список, внутри строки, 158

        ##    названия
        for a in data:
            name = re.findall(r'name-ind">(.*?) — <b>', a)
            names.append(name) ## список, внутри списки, в каждом по строке с именем или пусто, 158            

        ##    номера томов     
            volumes = re.findall(r'[IV]+', a) ## для каждой строки - список, такой: ['IV'],
            ## такой: ['II', 'IV'] или такой: []
            vol.append(volumes)

        ## номера страниц
            vol_p = re.split(r'[IV]+', a) ##  часть строки между римскими цифрами
            del vol_p[0]
            pg = [re.findall(r'\d+[;,-]?\d+', element) for element in vol_p]
            pg1.append(pg)
##            print(pg) ## для каждой строки – список, такой:
            ## ['61', '366'], если один том, или больше – по числу томов: [['270'], ['190']]


        ##    ИТОГ
##        print(names[-3])  ## ['Юдифь']
##        print(vol[-3])  ## ['I', 'II']
##        print(pg1[3]) ## [['94', '244'], ['482', '573']]       
                       
            for i in range(len(volumes)):                    
                if volumes[i]==volume_n_roman:
                    if pg:
                        for f in pg[i]:
                            if page_n:
                                for u in range(len(page_n)):
                                    if f==page_n[u]:                                       
                                        for y in range(len(name[0])-3):                                        
                                            if name[0][:-(y+1)] in sourcecode:                                        
                                                tagged_name = re.search(name[0][:-(y+1)]+'[а-яА-Я]*', sourcecode)
                                                if tagged_name:
                                                    myth_names.append(tagged_name.group())
                                                    myth_names1.append(name[0])
                                                    break
                                    else:
                                        try:
                                            if int(f[-3:])==int(page_n_1)+1:                                         
                                                for y in range(len(name[0])-3):                                        
                                                    if name[0][:-(y+1)] in sourcecode:                                        
                                                        tagged_name = re.search(name[0][:-(y+1)]+'[а-яА-Я]*', sourcecode)                                            
                                                        myth_names.append(tagged_name.group())
                                                        myth_names1.append(name[0])
                                                        break
                                        except:
                                            continue
                            else:
                                try:
                                    if int(f[-3:])==int(page_n_1)+1:                                         
                                        for y in range(len(name[0])-3):                                        
                                            if name[0][:-(y+1)] in sourcecode:                                        
                                                tagged_name = re.search(name[0][:-(y+1)]+'[а-яА-Я]*', sourcecode)                                            
                                                myth_names.append(tagged_name.group())
                                                myth_names1.append(name[0])
                                                break
                                except:
                                    continue
            

## Указатель географических названий

        vol_page = []
        names = []
        newnames = []
        newname = []
        data = []
        vol = []
        pg = []
        pg1 = []
        names_2 = []
        name_2 = []
        geo_names = []
        geo_names1 = []
        geo_names_2 = []
        geo_names1_2 = []
        f_name = []
        g_names = []
        g_names_2 = []


        with open('geohistory_index.htm', 'r', encoding='cp1251') as page:
            lines = page.readlines() ## построчный список вида ['str1', 'str2'...]
            for line in lines:

        ##        вся строка с данными
                line_data = re.findall(r'(<p class="name-ind">.*?</p>)', line)
                if line_data:
                    if '&nbsp;' not in line_data:
        ##                print(line_data) ## например:
                        ## ['<p class="name-ind">Япония — <b>II:</b> 270; <b>III:</b> 190']
                        for j in line_data:
                            data.append(j) ## список, внутри строки, 423               

        ##    названия
        for a in data:
            name = re.findall(r'name-ind">(.*?) — <b>', a)
            if name:
                if '<br>' in name[-1]:
                    name = g_names[-1] ## обработали два исключения (Петербург и Рим)
            g_names.append(name) ## список, внутри списки, в каждом по строке с именем или пусто, 423
            
        ##    названия второго порядка
            name_2 = re.findall(r'.*?<br>\s?(.*?) — <b>', a)
##            print(len(name_2)) ## список, внутри списки, в каждом строки с именами или пусто, 423

        ##    номера томов     
            volumes = re.findall(r'[IV]+', a)
            vol.append(volumes) ## для каждой строки - список, такой: ['IV'],
            ## такой: ['II', 'IV'] или такой: [], 423

        ## номера страниц
            vol_p = re.split(r'[IV]+', a) ##  часть строки между римскими цифрами
            del vol_p[0]
            pg = [re.findall(r'\d+[;,-]?\d+', element) for element in vol_p]
##            print(pg)
            pg1.append(pg)
        ##print(pg1) ## список, внутри 423 списка по числу статей, внутри один список: ['61', '366'],
        ## если один том, или больше – по числу томов: [['270'], ['190']]

##        ##    ИТОГ
##        print(g_names[105])  ## ['Царское (Детское) Село (г. Пушкин)']
##        print(g_names_2[105])  ## [' Китайская деревня']
##        print(vol[105])  ## ['I', 'II', 'IV', 'IV']
##        print(pg1[105]) ## [['76', '239'], ['485'],
##        ## ['13', '44', '53', '61', '62', '72', '77', '78', '81', '82', '84-88', '92', '93', '95'],
##        ## ['53', '83', '84', '88']]

            ## для каждой строки геосписка...
            for i in range(len(volumes)): ## по числу томов в строке указателя
                if volumes[i]==volume_n_roman: ## если том соответствует тому пр-ния
                    for f in pg[i]: ## по числу номеров страниц в указателе (соответствующих опред. тому)
                            if page_n:  ## если в нашем файле есть номер страницы                                    
                                for u in range(len(page_n)): ## по числу номеров страниц в нашем файле
                                    if f==page_n[u]: ## если номер страницы в указателе совпадает с номером в файле                                             
                                        for elem in auth_text:
                                            for y in range(len(name[0])-3):
                                                ## по числу букв названия из указателя минус три                                            
                                                if name[0][:-(y+1)] in elem:
                                                    ## если это название, уменьшающееся постепенно, есть в тексте пр-ния
                                                    if name[0][:-(y+1)] not in geo_names:                                                    
                                                        geo_names.append(name[0][:-(y+1)])
                                                        geo_names1.append(name[0]) ## и сюда целое имя из указателя
                                                        break
                                                    break
                                            
                                        if name_2:  ## если есть названия второго порядка
                                            for j in name_2: ## для каждого из этих названий
                                                for elem in auth_text:
                                                    for l in range(len(j)-4):
                                                        ## по числу букв названия второго порядка минус четыре                                                    
                                                        if j[:-(l+1)] in elem:
                                                            ## если это название, уменьшающееся постепенно, есть в тексте пр-ния                                                        
                                                            if j[:-(l+1)] not in geo_names_2:
                                                                geo_names_2.append(j[:-(l+1)])
                                                                geo_names1_2.append(name[0]) ## и сюда целое имя из указателя
                                                                break
                                                            break                                    
                                                                
                                    else: ## если номер страницы в указателе не совпадает с номером в файле
                                        if int(f[-3:])==int(page_n[-1])+1:
                                            ## если номер из геосписка равен посл. номеру нашей страницы плюс единица                                                    
                                            for elem in auth_text:
                                                for y in range(len(name[0])-3): ## по числу букв названия из геосписка минус три                                                
                                                    if name[0][:-(y+1)] in elem:
                                                        ## если это название, уменьшающееся постепенно, есть в тексте пр-ния
                                                        if name[0][:-(y+1)] not in geo_names:
                                                            geo_names.append(name[0][:-(y+1)])
                                                            geo_names1.append(name[0]) ## и сюда целое имя из указателя
                                                            break
                                                        break 

                                            if name_2:  ## если есть названия второго порядка
                                                for j in name_2: ## для этих названий
                                                    for elem in auth_text:
                                                        for l in range(len(j)-4):
                                                            ## по числу букв названия второго порядка минус четыре                                                        
                                                            if j[:-(l+1)] in elem:
                                                                ## если это название, уменьшающееся постепенно, есть в тексте пр-ния
                                                                if j[:-(l+1)] not in geo_names_2:
                                                                    geo_names_2.append(j[:-(l+1)])
                                                                    geo_names1_2.append(name[0]) ## и сюда целое имя из указателя
                                                                    break
                                                                break                                                             

                            else: ## если у нас нет номера страницы пр-ния
                                try: ## пробуем
                                    if int(f[-3:])==int(page_n_1[-1])+1:
                                        ## если номер из геосписка равен номеру страницы предыдущего файла плюс единица
                                        for elem in auth_text:
                                            for y in range(len(name[0])-3): ## по числу букв названия из геосписка минус три                                            
                                                if name[0][:-(y+1)] in elem:
                                                    ## если это название, уменьшающееся постепенно, есть в тексте пр-ния
                                                    if name[0][:-(y+1)] not in geo_names:
                                                        geo_names.append(name[0][:-(y+1)])
                                                        geo_names1.append(name[0]) ## и сюда целое имя из указателя
                                                        break
                                                    break
                                                                                   
                                        if name_2: ## если есть названия второго порядка
                                            for j in name_2: ## для этих названий
                                                for elem in auth_text:
                                                    for l in range(len(j)-4): ## по числу букв названия второго порядка минус четыре                                                    
                                                        if j[:-(l+1)] in elem:
                                                            ## если это название, уменьшающееся постепенно, есть в тексте пр-ния
                                                            if j[:-(l+1)] not in geo_names_2:
                                                                geo_names_2.append(j[:-(l+1)])
                                                                geo_names1_2.append(name[0]) ## и сюда целое имя из указателя
                                                                break
                                                            break 
                                except:
                                    continue


## Указатель имён

        vol_page = []
        names = []
        data = []
        vol = []
        pg = []
        pg1 = []
        name_names = []
        name_names1 = []
        n_names = []


        with open('name_index.htm', 'r', encoding='cp1251') as page:
            lines = page.readlines() ## построчный список вида ['str1', 'str2'...]
            for line in lines:

        ##        вся строка с данными
                line_data = re.findall(r'(<p class="name-ind">.*?</p>)', line)
                if line_data:
                    if '&nbsp;' not in line_data:
##                        print(line_data) ## например:
        ## ['<p class="name-ind"><i>Айзенштадт, А.Г.</i>, скрипач — <b>III:</b> 47, 310</p>']
                        for j in line_data:
                            data.append(j) ## список, внутри строки, 1226

        ##    имена людей
        for a in data:
            name = re.findall(r'name-ind"><i>(.*?)</i>', a)
            names.append(name) ## список, внутри списки, в каждом по строке с именем или пусто, 1226

        ##    номера томов     
            volumes = re.findall(r'[IV]+', a) ## для каждой строки - список, такой: ['IV'],
            ## такой: ['II', 'IV'] или такой: []
            vol.append(volumes) ##  1226
            
        ## номера страниц
            vol_p = re.split(r'[IV]+', a) ##  часть строки между римскими цифрами
            del vol_p[0]
            pg = [re.findall(r'\d+[;,-]?\d+', element) for element in vol_p]
            pg1.append(pg)
##            print(pg) ## для каждой строки – список: [['61']] или [['270'], ['190']]


        ##    ИТОГ
##        print(names[-2])  ## ['Янсон Я. Д.,']
##        print(vol[-2])  ## ['IV']
##        print(pg1[-2]) ## [['95', '388']]

            for i in range(len(volumes)):  ## по числу томов в строке именного указателя
                if volumes[i]==volume_n_roman: ## если номер тома соответствует нашему
                    for f in pg[i]: ## по числу номеров страниц в указателе (соответствующих опред. тому)
                        if page_n: ## если в нашем файле есть номер страницы
                            for u in range(len(page_n)): ## по числу номеров страниц в нашем файле
                                if f==page_n[u]: ## если номер в указателе совпадает с номером в файле                                                                            
                                    for elem in auth_text: ## по абзацам нашего произведения
                                        for y in range(len(name[0])-3): ## по числу букв названия из указателя минус три
                                            if name[0][:-(y+1)] in elem:
                                                ## если это название, уменьшающееся постепенно, есть в строке пр-ния                                            
                                                if name[0][:-(y+1)] not in name_names:
                                                    name_names.append(name[0][:-(y+1)])
                                                    name_names1.append(name[0]) ## и сюда целое имя из указателя
                                                    break
                                                break
                                                                                                                                                           
                                else:  ## если номер в указателе не совпадает с номером в файле 
                                    if int(f[-3:])==int(page_n[-1])+1:
                                        ## если номер из указателя равен посл. номеру нашей страницы плюс единица                                         
                                        for elem in auth_text:
                                            for y in range(len(name[0])-3): ## по числу букв названия из указателя минус три                                            
                                                if name[0][:-(y+1)] in elem:
                                                    ## если это название, уменьшающееся постепенно, есть в тексте пр-ния
                                                    if name[0][:-(y+1)] not in name_names:
                                                        name_names.append(name[0][:-(y+1)])
                                                        name_names1.append(name[0]) ## и сюда целое имя из указателя
                                                        break
                                                    break

                        else: ## если в нашем файле вообще нет номера страницы
                            try:
                                if int(f[-3:])==int(page_n_1[-1])+1:
                                    ## если номер из геосписка равен номеру страницы предыдущего файла плюс единица
                                    for elem in auth_text:
                                        for y in range(len(name[0])-3): ## по числу букв названия из указателя минус три                                        
                                            if name[0][:-(y+1)] in elem:
                                                ## если это название, уменьшающееся постепенно, есть в тексте пр-ния
                                                if name[0][:-(y+1)] not in name_names:
                                                    name_names.append(name[0][:-(y+1)])
                                                    name_names1.append(name[0]) ## и сюда целое имя из указателя
                                                    break
                                                break

                            except:
                                continue

                                
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
        
##    номер строки, если это стихи
##    (список, элементы которого – номера всех строк, например, [1, 2, 3, 4])
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
##                print(couplet_num) ## для каждой строфы – список вида
                ## ['L1', 'L2', 'L3', 'L4']
                if not couplet_num:
                    couplet_num = tree.xpath('//div[@class]//span[@class]/@id')
##                print(couplet_num) ## для всего стихотворения список вида
                    ## ['L1', 'L2', 'L3', 'L4']
                
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
##            print(len_coup) ## len_coup для стихотворения - список чисел,
    ## соответствующих числу строк в каждой строфе, например [4, 4, 4, 4, 2] OK
##
##                    информация о каждой строфе: собственно стихи в виде списка                  
                if int(verse_num[-1][-1])>1:
                    couplet_text = tree.xpath('//p[@id="st{0}"]//span[@class]/text()'.format(x+1))                    
                else:
##!                    couplet_text = tree.xpath('//span[@class]/text()')
                    couplet_text = re.findall(r'<span class="line.+?[\d]">(.+?)</span', sourcecode)
##                    print(couplet_text)                    
                coup_text.append(couplet_text)
##            print(coup_text) ## coup_text - общий список, в который вложены подсписки
            ## по числу строф, элементы каждого подсписка – это отдельные стихи (в виде строк)
                           
##        собственно текст, если это стихи (все строки стихотворения в виде списка)
        verse_text = tree.xpath('.//span[@class="line"]/text() | \
.//span[@class="line1r"]/text()')
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
            if name_names:
                
                for p in range(len(name_names)):
                    if name_names[p] in ''.join(dedication):
                        rs = etree.SubElement(div2, 'rs', type = 'person', ref = name_names1[p])
                        break

        if epigraph: ## эпиграф
            epig = etree.SubElement(div2, 'epigraph')

        if epigraph: ## эпиграф
            epig_quot = etree.SubElement(epig, 'quote').text = ''.join(epigraph)

        if epigraph_src: ## эпиграф: автор
            epi_src = etree.SubElement(epig, 'bibl').text = ''.join(epigraph_src)
            if name_names:
                for p in range(len(name_names)):
                        if name_names[p] in ''.join(dedication):
                            rs = etree.SubElement(div2, 'rs', type = 'person', ref = name_names1[p])
                            break
            
        if poem:
            k = 0
            c = 0
            for i in range(len(verse_num)):  ## число строф
                lg = etree.SubElement(div2, 'lg', type = '{}'.format(tei_coup_num[i])) \
                     ## название, например, sestet
                for s in range(len_coup[i]):  ## число строк в строфе
                    l = etree.SubElement(lg, 'l', n = str(linelist[k])) \
                    ## сам текст: стихи                                        
                    if myth_names:
                        for p in range(len(myth_names)):
                            if myth_names[p] in coup_text[i][s]:                                
                                rs = etree.SubElement(l, 'rs', type = 'myth_index', ref = myth_names1[p])
                    l.text = coup_text[i][s]
                    k += 1
                    if geo_names:
                        for m in range(len(geo_names)):
                            if geo_names[m] in coup_text[i][s]:
                                rs = etree.SubElement(l, 'rs', type = 'geo_index', ref = geo_names1[m])
                                break
                    if geo_names_2:
                        for h in range(len(geo_names_2)):
                            if geo_names_2[h] in coup_text[i][s]:
                                rs = etree.SubElement(l, 'rs', type = 'geo_index', ref = geo_names1_2[h])
                                break
                    if name_names:
                        for p in range(len(name_names)):
                            if name_names[p] in coup_text[i][s]:                                
                                rs = etree.SubElement(l, 'rs', type = 'person', ref = name_names1[p])
                                break
##                    if poemlasttxt:
##                        for t in poemlasttxt:
##                            if coup_text[i][s]==t:
##                                pb = etree.SubElement(div2, 'pb').text = page[c]
                    ## номера страниц
##                            else:
##                                continue
##                            c += 1
                            
        if not poem:
            c = 0
            for m in range(len(paragraph)): ## число абзацев
                p1 = etree.SubElement(div2, 'p') ## проза: текст
                if myth_names:
                    for p in range(len(myth_names)):
                        if myth_names[p] in paragraph[m]:                                
                            rs = etree.SubElement(p1, 'rs', type = 'myth_index', ref = myth_names1[p])
##                            break
                if geo_names:
                    for h in range(len(geo_names)):
                        if geo_names[h] in paragraph[m]:
                            rs = etree.SubElement(p1, 'rs', type = 'geo_index', ref = geo_names1[h])
##                            break
                if geo_names_2:
                    for d in range(len(geo_names_2)):                               
                        if geo_names_2[d] in paragraph[m]:
                            if 'Петербург' not in geo_names1_2[d]:
                                rs = etree.SubElement(p1, 'rs', type = 'geo_index', ref = geo_names1_2[d])
##                                break
                if name_names:
                    for p in range(len(name_names)):
                        if name_names[p] in paragraph[m]:                            
                            rs = etree.SubElement(p1, 'rs', type = 'person', ref = name_names1[p])
##                            break
                p1.text = paragraph[m]
##                for z in plasttxt:
##                    if paragraph[m] == z:
##                        pb = etree.SubElement(div2, 'pb').text = page[c] ## номера страниц
##                        ## в нужном месте (проза, письма)
##                    else:
##                        continue
##                    c += 1        

        if full_date and not full_date_from and not full_date_to:
            for s in full_date:
                datelist = []
                date_join = s.get('y', ''), s.get('m', ''), s.get('d', '') ## (['1911'], ['11'], ['24', '26'])
                for u in date_join:
                    if u:
                        k = ', '.join(u)
                        datelist.append(k)
                dateline = etree.SubElement(div2, 'date', when = '-'.join(datelist)).text = date[0]

        if full_date_from and full_date_to:
            date_from_list = []
            date_to_list = []
            date_from_join = full_date_from.get('y', ''), full_date_from.get('m', ''), full_date_from.get('d', '')
            date_to_join = full_date_to.get('y', ''), full_date_to.get('m', ''), full_date_to.get('d', '')
            for u in date_from_join:
                if u:
                    k = ''.join(u)
                    date_from_list.append(k)
            for u in date_to_join:
                if u:
                    k = ''.join(u)
                    date_to_list.append(k)                                        
            myattr = {'from':'-'.join(date_from_list), 'to': '-'.join(date_to_list)}
            dateline = etree.SubElement(div2, 'date', attrib = myattr).text = date[0]

        if full_date_to and not full_date_from:
            date_to_list = []
            date_to_join = full_date_to.get('y', ''), full_date_to.get('m', ''), full_date_to.get('d', '')
            for u in date_to_join:
                if u:
                    k = ''.join(u)
                    date_to_list.append(k)                                        
            myattr = {'to': '-'.join(date_to_list)}
            dateline = etree.SubElement(div2, 'date', attrib = myattr).text = date[0]


        if full_date_to and len(full_date) > 1:
            if not worm_mark:
                for s in full_date:
                    datelist = []
                    date_join = s.get('y', ''), s.get('m', ''), s.get('d', '') ## (['1911'], ['11'], ['24', '26'])
                    for u in date_join:
                        if u:
                            k = ', '.join(u)
                            datelist.append(k)
                dateline = etree.SubElement(div2, 'date', when = '-'.join(datelist)).text = date[0]
                
##        if full_date_from:
##            print(date[0])
##            print(full_date_from)
##            print('--------')
##            myattr = {'from':'-'.join(full_date_from), 'to': '-'.join(full_date_to)}
##            dateline = etree.SubElement(div2, 'date', attrib = myattr).text = date[0]
                       
##            if year:
##               if full_date:
##                   dateline = etree.SubElement(div2, 'date', when = '#'.join(year) \
##                                           , precision = "circa").text = date[0]

            for w in g_names:
                try:
                    if w[0][:3] in date[0]:
                        rs = etree.SubElement(div2, 'rs', type = 'geo_index', ref = w[0])                        
                except:
                    continue

##        if full_date_to:
##            print(date[0])
##            print(full_date_to)
##            print('--------')

        if date: ## географические названия в датах
            for w in g_names:
                if w:
                    f_name = re.search(r'(\S+)', w[0])
                    if f_name.group() in date[0]: ## если это название (первое слово целиком) есть в тексте даты пр-ния
                        if 'Ганг' not in f_name.group() and 'Луга' not in f_name.group() and 'После' not in date[0]:
                            rs = etree.SubElement(div2, 'rs', type = 'geo_index', ref = w[0])            
                            break
                        
            if 'Гельсингфорс' in date[0]:
                rs = etree.SubElement(div2, 'rs', type = 'geo_index', ref = 'Хельсинки (Гельсингфорс)')
                                                  
        if note:
            nte = etree.SubElement(div2, 'note').text = ''.join(note) ## ссылка
            if myth_names:
                for p in range(len(myth_names)):
                    if myth_names[p] in ''.join(note):                                
                        rs = etree.SubElement(div2, 'rs', type = 'myth_index', ref = myth_names1[p])
##                            break

            if geo_names:
                for h in range(len(geo_names)):
                    if geo_names[h] in ''.join(note):
                        rs = etree.SubElement(div2, 'rs', type = 'geo_index', ref = geo_names1[h])
##                            break
            if geo_names_2:
                for d in range(len(geo_names_2)):                               
                    if geo_names_2[d] in ''.join(note):
                        rs = etree.SubElement(div2, 'rs', type = 'geo_index', ref = geo_names1_2[d])
##                                break
            
            if name_names:
                for p in range(len(name_names)):
                    if name_names[p] in ''.join(note):                            
                        rs = etree.SubElement(div2, 'rs', type = 'person', ref = name_names1[p])
                        break
                                               
        tree = etree.ElementTree(tei)
        tree.write(path_2+file[:-4]+'.xml', encoding = 'utf8', pretty_print = True, \
                   xml_declaration = True)
