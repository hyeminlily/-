from bs4 import BeautifulSoup
import cx_Oracle as oc
import os
import requests
import re

# get max page number
url_list = 'http://cinefox.com/vod/movie/list'
rq = requests.request("GET", url_list)
html = BeautifulSoup(rq.content, 'html.parser')
wrapper = html.find('div', {'class': 'paginate wrapper'})
li = wrapper.findAll('li')
max = li[-1].text
max = int(max.replace('...', ''))

# get movie info from Cinefox
for page in range(max):
    url = 'http://clean.cinefox.com/vod/movie/list?page=' + str(page + 1)
    result = requests.get(url=url, timeout=10)
    data = BeautifulSoup(result.content, 'html.parser')

    div = data.findAll('div', {'class': "postimg"})
    no_list = re.findall('<.+?onclick="aram.move(.+?)">', str(div))

    for movie_no in no_list:
        # get no
        movie_no = movie_no.split('=')[1]
        movie_no = movie_no.split("\'")[0]

        # get detail info
        url_dt = 'http://clean.cinefox.com/vod/view?product_seq=' + movie_no
        result_dt = requests.get(url=url_dt, timeout=10)
        data_dt = BeautifulSoup(result_dt.content, 'html.parser')

        # get title, titleEng
        title = data_dt.find('span', {'class': 'title'}).text.strip()
        print(title)
        titleEng = data_dt.find('span', {'class': 'titleEnglish'}).text.strip()

        # divide infoWrap
        meta_info = data_dt.find('div', {'class': 'metaInfoWrap'})
        div_list = meta_info.findAll('div')
        info_spec = div_list[0]
        plp_list = div_list[1]

        spec_list = re.sub('\t|\r|\n', '', str(info_spec))
        spec_list = spec_list.replace('<div>', '')
        spec_list = spec_list.replace('<span>', '')
        spec_list = spec_list.replace('</span>', '')

        split = spec_list.split('|')

        # get runtime
        runtime = ''
        if len(split) > 0:
            runtime = split[0]

        # get nation
        nation = ''
        if len(split) > 1:
            nation = split[1]
            nation = nation.replace(',', ', ')

        # get genre
        genre = ''
        if len(split) > 2:
            genre = split[2]
            genre = genre.replace(',', ', ')

        # get opendate & grade
        opendate = ''
        grade = ''
        if len(split) > 3 and split[3].split(' ')[0] == '개봉':
            opendate = split[3]
            opendate = opendate.replace('개봉 ', '')
            opendate = opendate.replace('-', '/')
            grade = split[4]
            grade = grade.replace('</div>', '')
        elif len(split) > 3 and split[3].split(' ')[0] != '개봉':
            grade = split[3]
            grade = grade.replace('</div>', '')

        # get director
        director = str(plp_list).split('<span>')[0]
        director = re.sub('\t|\r|\n', '', director)
        director = director.replace('<div>', '')
        director = director.replace('감독 : ', '')
        director = director.replace(',', ', ')
        director = director.strip()

        # get actor
        actor = str(plp_list).split('<span>')[1]
        actor = re.sub('\t|\r|\n', '', actor)
        actor = actor.replace('</span>', '')
        actor = actor.replace('</div>', '')
        actor = actor.replace('|', '')
        actor = actor.replace('주연 : ', '')
        actor = actor.replace(',', ', ')
        actor = actor.strip()

        # get poster image
        img_src = data_dt.find('img', {'id': "PIMG"})['src']
        if img_src == '/Modules/storeFox/_view/skin/prodcutView/w_default_v1/images/ageposter_L.png':
            img_src = 'http://cinefox.com/Modules/storeFox/_view/skin/prodcutView/w_default_v1/images/ageposter_L.png'

        # get content
        content = ''
        contents = ''
        div_cont = data_dt.find('div', {'id': "content"})
        all_p = div_cont.findAll('p')

        for ap in all_p:
            ap = ap.text.strip()
            contents += ap + '<br>'

        if len(contents) >= 1900:
            content = contents.split('<br>')[0]
            print(movie_no, content)
        elif 1900 > len(contents) >= 1750:
            content = contents.split('<br><br>')[0]
            print(movie_no, content)
        else:
            content = contents

        # Oracle Connection - insert
        os.environ["NLS_LANG"] = ".AL32UTF8"
        START_VALUE = u"Unicode \u3042 3".encode('utf-8')
        END_VALUE = u"Unicode \u3042 6".encode('utf-8')

        conn = oc.connect('hyeminseo/hyeminseo@203.236.209.97:1521/XE')
        cursor = conn.cursor()
        cursor.execute('insert into movies values(:movie_no, :movie_title, :movie_titleEng, :movie_genre, :movie_nation, :movie_runtime, :movie_grade, :movie_opendate, :movie_director, :movie_actor, :movie_image_url, :movie_play_url, :movie_content)',
                       movie_no=int(movie_no), movie_title=title, movie_titleEng=titleEng, movie_genre=genre, movie_nation=nation, movie_runtime=runtime,
                       movie_grade=grade, movie_opendate=opendate, movie_director=director, movie_actor=actor, movie_image_url=img_src, movie_play_url=url_dt,
                       movie_content=content)
        conn.commit()
        cursor.close()
        conn.close

