from bs4 import BeautifulSoup
import requests
import re
import tving_crowl_func

title_list = tving_crowl_func.getTitleList()
for t in title_list:
    t = t.replace(" ", "+")

    # search in Naver with movie title from Tving and Cinefox
    url = 'https://movie.naver.com/movie/search/result.nhn?query=' + t + "&section=all&ie=utf8"
    result = requests.get(url)
    html = BeautifulSoup(result.content, 'html.parser')

    if html.find('ul', {'class': "search_list_1"}) != None:
        ul = html.find('ul', {'class': "search_list_1"})
        no = ul.find('a')['href'].split("/")[-1].split("=")[-1]
        play_url = 'https://series.naver.com/tvstore/detail.nhn?mcode=' + no

        # get movie basic info
        url_mv = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=' + no
        result_mv = requests.get(url_mv)
        html_mv = BeautifulSoup(result_mv.content, 'html.parser')
        info = html_mv.find('div', {'class': "mv_info"})

        # get title, titleEng
        title = info.find('h3', {'class': "h_movie"}).find('a').text
        titleEng = info.find('strong', {'class': "h_movie2"}).text
        titleEng = re.sub('\t|\r|\n', '', titleEng)
        rm_year = re.findall('[0-9][0-9][0-9][0-9]', titleEng)
        titleEng = titleEng.replace(', ' + rm_year[0], '')
        titleEng = titleEng.replace(rm_year[0], '')

        # get genre, nation, runtime
        info_spec = html_mv.find('dl', {'class': 'info_spec'})
        dd = info_spec.findAll('dd')

        genre = ''
        genre_list1 = dd[0].findAll('span')[0]
        genre_list2 = genre_list1.findAll('a')
        for g in genre_list2:
            gt = g.text
            if g == genre_list2[-1]:
                genre += gt
            else:
                genre += gt + ', '

        nation = ''
        nation_list1 = dd[0].findAll('span')[1]
        nation_list2 = genre_list1.findAll('a')
        for n in nation_list2:
            nt = n.text
            if n == nation_list2[-1]:
                nation += nt
            else:
                nation += nt + ', '

        runtime = dd[0].findAll('span')[2].text.strip()

        # get opendate
        if len(dd[0].findAll('span')) > 3:
            year = dd[0].findAll('span')[3].findAll('a')
            split_year1 = str(year).split('>')
            split_year2 = split_year1[1].split('<')[0].strip()
            split_year3 = split_year1[3].split('<')[0]
            opendate = split_year2 + split_year3
            opendate = opendate.replace('.', '/')
        else:
            opendate = ''

        # get age
        if len(dd) > 3:
            age = dd[3].find('a').text
        elif len(dd) == 3:
            age = dd[2].find('a').text
        else:
            age = ''

        # get content
        story_area = html_mv.find('div', {'class': 'story_area'})
        head = re.findall('<h5 class="h_tx_story">(.+?)</h5>', str(story_area))
        contents = re.findall('<p class="con_tx">(.+?)</p>', str(story_area))
        if len(contents) >= 1:
            contents[0] = contents[0].replace('\r', '')
            contents[0] = contents[0].replace('\xa0', '')
            if len(head) != 0:
                content = head[0] + '<br/>' + contents[0]
            else:
                content = contents[0]
        else:
            content = ''

        # get poster image
        poster = html_mv.find('div', {'class': "poster"})
        img_src = poster.find('img')['src']
        src = requests.get(img_src)
        fname = no + '.jpg'
        img_file = 'C:/stsTest/2M_Project/src/main/webapp/resources/images/' + fname

        file = open(img_file, 'wb')
        file.write(src.content)
        file.close()

        # get movie detail info
        url_dt = 'https://movie.naver.com/movie/bi/mi/detail.nhn?code=' + no
        result_dt = requests.get(url_dt)
        html_dt = BeautifulSoup(result_dt.content, 'html.parser')

        # get director list
        directors = html_dt.find('div', {'class': "director"})
        directors_list = re.findall('<a class="k_name" href=".+?" title=".+?">(.+?)</a>', str(directors))
        director = ''
        for dir in directors_list:
            if dir == directors_list[-1]:
                director += dir
            else:
                director += dir + ', '

        # get actor list
        actors = html_dt.find('div', {'class': "made_people"})
        actors_list = re.findall('<a class="k_name" href=".+?" title=".+?">(.+?)</a>', str(actors))
        actor = ''
        if len(actors_list) != 0:
            for act in actors_list:
                if act == actors_list[-1]:
                    actor += act
                else:
                    actor += act + ', '

    # print(no, ' / ', title, ' / ', titleEng, ' / ', genre, ' / ', nation, ' / ', runtime, ' / ', age, ' / ', director, ' / ', actor, ' / ', opendate, ' / ', content, ' / ', fname, ' / ', play_url)