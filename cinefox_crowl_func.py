from bs4 import BeautifulSoup
import requests
import re

def getTitleList():
    # get movie info from Cinefox
    for page in range(234):
        url = 'http://clean.cinefox.com/vod/movie/list?page=' + str(page + 1)
        result = requests.get(url)
        data = BeautifulSoup(result.content, 'html.parser')

        div = data.findAll('div', {'class': "postimg"})
        no_list = re.findall('<.+?onclick="aram.move(.+?)">', str(div))

        for movie_no in no_list:
            # get no
            movie_no = movie_no.split('=')[1]
            movie_no = movie_no.split("\'")[0]

            # get detail info
            url_dt = 'http://clean.cinefox.com/vod/view?product_seq=' + movie_no
            result_dt = requests.get(url_dt)
            data_dt = BeautifulSoup(result_dt.content, 'html.parser')

            # get title, titleEng
            title = data_dt.find('span', {'class': 'title'}).text.strip()
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

            # get runtime
            runtime = spec_list.split('|')[0]

            # get nation
            nation = spec_list.split('|')[1]
            nation = nation.replace(',', ', ')

            # get genre
            genre = spec_list.split('|')[2]
            genre = genre.replace(',', ', ')

            # get opendate
            opendate = spec_list.split('|')[3]
            opendate = opendate.replace('개봉 ', '')
            opendate = opendate.replace('-', '/')

            # get grade
            grade = spec_list.split('|')[4]

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

            print(movie_no)
            print(title)
            print(titleEng)
            print(runtime)
            print(nation)
            print(genre)
            print(opendate)
            print(grade)
    # return title_list

getTitleList()