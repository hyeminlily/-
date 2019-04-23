from bs4 import BeautifulSoup
import requests
import re

def getMovieList():
    movies = []

    # get movie info from Cinefox
    for page in range(234):
        url = 'http://clean.cinefox.com/vod/movie/list?page=' + str(page + 1)
        result = requests.get(url)
        data = BeautifulSoup(result.content, 'html.parser')

        div = data.findAll('div', {'class': "postimg"})
        no_list = re.findall('<.+?onclick="aram.move(.+?)">', str(div))

        for movie_no in no_list:
            movie = []

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

            # get poster image
            img_src = data_dt.find('img', {'id': "PIMG"})['src']
            img = requests.get(img_src)
            fname = movie_no + '.jpg'
            img_file = 'C:/stsTest/2M_Project/src/main/webapp/resources/poster/' + fname

            file = open(img_file, 'wb')
            file.write(img.content)
            file.close()

            # get content
            div_cont = data_dt.find('div', {'id': "content"})
            content = ''
            all_p = div_cont.findAll('p')
            for ap in all_p:
                ap = ap.text.strip()
                ap = ap.replace('\u200b', '')
                content += ap + '<br>'
            content = content[:4]

            movie.append(movie_no)
            movie.append(title)
            movie.append(titleEng)
            movie.append(genre)
            movie.append(nation)
            movie.append(runtime)
            movie.append(grade)
            movie.append(opendate)
            movie.append(director)
            movie.append(actor)
            movie.append(fname)
            movie.append(url_dt)
            movie.append(content)
            movies.append(movie)
    return movies