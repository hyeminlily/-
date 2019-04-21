from bs4 import BeautifulSoup
import requests
import re
import tving_crowl_func

def getMovieList():
    movies = []
    title_list = tving_crowl_func.getTitleList()
    for t in title_list:
        movie = []
        t = t.replace(" ", "+")

        # search in Naver with movie title from Tving and Cinefox
        url = 'https://movie.naver.com/movie/search/result.nhn?query=' + t + "&section=all&ie=utf8"
        result = requests.get(url)
        html = BeautifulSoup(result.content, 'html.parser')

        if html.find('ul', {'class': "search_list_1"}) != None:
            ul = html.find('ul', {'class': "search_list_1"})
            no = ul.find('a')['href'].split("/")[-1].split("=")[-1]
            movie.append(no)

            # get movie basic info
            url_mv = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=' + no
            result_mv = requests.get(url_mv)
            html_mv = BeautifulSoup(result_mv.content, 'html.parser')
            info = html_mv.find('div', {'class': "mv_info"})

            # get title, titleEng
            title = info.find('h3', {'class': "h_movie"}).find('a').text
            movie.append(title)

            titleEng = info.find('strong', {'class': "h_movie2"}).text
            titleEng = re.sub('\t|\r|\n', '', titleEng)
            rm_year = re.findall('[0-9][0-9][0-9][0-9]', titleEng)
            titleEng = titleEng.replace(', ' + rm_year[0], '')
            titleEng = titleEng.replace(rm_year[0], '')
            movie.append(titleEng)

            # get genre, nation, runtime, grade, opendate
            info_spec = html_mv.find('dl', {'class': 'info_spec'})
            all_a_spec = info_spec.findAll('a')

            genre = ''
            nation = ''
            runtime = ''
            grade = ''
            opendate = ''

            for a in all_a_spec:
                if 'genre' in str(a):
                    at = a.text + ', '
                    genre += at

                if 'nation' in str(a):
                    at = a.text + ', '
                    nation += at

                if 'grade' in str(a):
                    grade += a.text
                    grade = grade.replace('G', '')
                    grade = grade.replace('P-13', '')
                    grade = grade.replace('PG-13', '')
                    grade = grade.replace('P', '')
                    grade = grade.replace('PG', '')
                    grade = grade.replace('R', '')
                    grade = grade.replace('NC-17', '')
                    grade = grade.replace('N', '청소년 관람불가')
                    grade = grade.replace('NR', '등급 보류')

                if 'open' in str(a):
                    at = a.text
                    opendate += at

            genre = genre[:-2]
            movie.append(genre)

            nation = nation[:-2]
            movie.append(nation)

            runtime_list = re.findall('<span>(.+?)분 </span>', str(info_spec))
            if len(runtime_list) > 0:
                runtime = runtime_list[0] + '분'
            movie.append(runtime)

            movie.append(grade)

            opendate = opendate.strip()
            opendate = opendate.replace('.', '/')
            movie.append(opendate)

            # get movie detail info
            url_dt = 'https://movie.naver.com/movie/bi/mi/detail.nhn?code=' + no
            result_dt = requests.get(url_dt)
            html_dt = BeautifulSoup(result_dt.content, 'html.parser')
            directors = html_dt.findAll('div', {'class': "dir_product"})
            actors = html_dt.findAll('div', {'class': "p_info"})

            # get director list
            director = ''
            for dts in directors:
                d_list = dts.findAll('a')
                for d in d_list:
                    if 'pi/basic' in str(d):
                        dt = d.text
                        director += dt + ', '
            director = director[:-2]
            movie.append(director)

            # get actor list
            actor = ''
            for ats in actors:
                a_list = ats.findAll('a')
                for ac in a_list:
                    if 'pi/basic' in str(ac):
                        at = ac.text
                        actor += at + ', '
            actor = actor[:-2]
            movie.append(actor)

            # get poster image
            poster = html_mv.find('div', {'class': "poster"})
            src = poster.find('img')['src']
            img = requests.get(src)
            fname = no + '.jpg'
            img_file = 'C:/stsTest/2M_Project/src/main/webapp/resources/poster/' + fname

            file = open(img_file, 'wb')
            file.write(img.content)
            file.close()
            movie.append(fname)

            play_url = 'https://series.naver.com/tvstore/detail.nhn?mcode=' + no
            movie.append(play_url)

            # get content
            story_area = html_mv.find('div', {'class': 'story_area'})
            head = re.findall('<h5 class="h_tx_story">(.+?)</h5>', str(story_area))
            contents = re.findall('<p class="con_tx">(.+?)</p>', str(story_area))
            content = ''
            if len(contents) > 0:
                contents[0] = contents[0].replace('\r', '')
                contents[0] = contents[0].replace('\xa0', '')
                if len(head) > 0:
                    content = head[0] + '<br/>' + contents[0]
                else:
                    content = contents[0]
            movie.append(content)
        movies.append(movie)
    return movies