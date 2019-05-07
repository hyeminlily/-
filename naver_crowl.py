import cx_Oracle as oc
import os
import urllib.request
import requests
import re
from bs4 import BeautifulSoup

# naver 영화 페이지 url
url = 'https://movie.naver.com/movie/running/current.nhn'
data = urllib.request.urlopen(url)
r = requests.get(url)

obj = BeautifulSoup(data, 'html.parser')
div = obj.find_all('div', {'class': 'thumb'})

no = []
for i in div:
    # 영화 상세페이지 링크
    '''[link]'''
    link1 = i.find('a')['href']
    link = 'https://movie.naver.com' + link1

    r1 = requests.get(link)
    obj2 = BeautifulSoup(r1.content, 'html.parser')

    # 영화 코드 추출
    '''[movino]'''
        # print(link1) => /movie/bi/mi/basic.nhn?code=164200
        # 위처럼 나와서 = 부터 마지막까지(-1) 잘라서 가져옴
    movino = link1.split('=')[-1]
    movino = movino.strip()

    # 한글 영화제목 추출
    '''[title]'''
    title1 = obj2.find('h3', {'class': 'h_movie'})
    title = title1.find('a').text.strip()

    # 영어 영화제목 추출
    '''[titleeng]'''

    titleeng1 = obj2.find('strong',{'class':'h_movie2'}).text.split(',')

    # split(,) 로 나누면 영문제목이 최대 2개의 , 로 나눠져있음. 그것을 list 길이로 구분해서 추출한 것
    if len(titleeng1) == 3:
        # , 두개로 나눠져있는 영문제목은 0번째 index와 1번째 index의 list를 하나로 합쳐주었음
        # strip은 양옆의 whitespace를 제거해준다.
        # 제거 안해주면 Call Me by Your\n\n\n\n\n\\n\ ,name\n\n\n\n\n\n\n 이런식으로 나움
        list1 = titleeng1[0].strip()
        list2 = titleeng1[1].strip()
        titleeng = list1+' , '+list2
    elif len(titleeng1) == 1:
        # 영문제목의 list의 길이 값이 1 인건 개봉 연도만 들어가있다는 말임.
        # 영문제목이 없기때문에 '' null값으로 넣어줌
        titleeng = ''
    else:
        titleeng = titleeng1[0].strip()
    titleeng = titleeng.strip()

    # 영화 배우(주연,조연) 이름 추출
    '''[actor]'''

    actor_url = 'https://movie.naver.com/movie/bi/mi/detail.nhn?code='+movino
    actor_r = requests.get(actor_url)
    actor_obj = BeautifulSoup(actor_r.content, 'html.parser')

    actor = ''
    if actor_obj.find('ul', {'class': "lst_people"}) != None:
        lst_people = actor_obj.find('ul', {'class': "lst_people"})
        actors = lst_people.findAll('div', {'class': "p_info"})
        for ats in actors:
            ac = ats.find('a').text
            actor += ac + ', '
        actor = actor[:-2]
    actor = actor.strip()

    # 영화 감독
    '''[director]'''

    dir_name = actor_obj.find('div', {'class': "dir_product"})
    director = dir_name.find('a', {'class': "k_name"}).text
    director = director.strip()

    # 영화 정보
    '''[opendate] [grade] [runtime] [nation] [genre]'''

    info_spec = obj2.find('dl', {'class': 'info_spec'})
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
            grade = grade.replace('NR', '')
            if grade == '':
                grade = '등급 보류'

            grade = grade.replace('G', '')
            grade = grade.replace('P-13', '')
            grade = grade.replace('PG-13', '')
            grade = grade.replace('P', '')
            grade = grade.replace('PG', '')
            grade = grade.replace('R', '')
            grade = grade.replace('NC-17', '')

        if 'open' in str(a):
            at = a.text
            opendate += at

    genre = genre[:-2]
    genre = genre.strip()

    nation = nation[:-2]
    nation = nation.strip()
    runtime_list = re.findall('<span>(.+?)분 </span>', str(info_spec))
    if len(runtime_list) > 0:
        runtime = runtime_list[0] + '분'
    runtime = runtime.strip()

    opendate = opendate.strip()
    opendate = opendate.replace('.', '/')
    opendate = opendate.strip()

    # 영화포스터
    '''[src]'''
    # poster = obj2.find('div', {'class': "poster"})
    # src = poster.find('img')['src']
    # src = src.strip()
    img_src = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + movino
    img_rslt = requests.get(img_src)
    img_html = BeautifulSoup(img_rslt.content, 'html.parser')
    src = img_html.find('img', {'id': 'targetImage'})['src']

    # 영화 영상 url
    '''[play_url]'''

    play = 'https://movie.naver.com/movie/bi/mi/media.nhn?code=' + movino
    r2 = requests.get(play)
    obj3 = BeautifulSoup(r1.content, 'html.parser')

    video_thumb = obj3.find('ul', {'class': 'video_thumb'})
    if video_thumb == None:
        play_href ==''
        play_url ==''
    else:
        play_href = video_thumb.find('a')['href']
        play_url = 'https://movie.naver.com'+play_href
    play_url = play_url.strip()

    # 영화 내용 추출
    '''[content]'''

    story_area = obj2.find('div', {'class': 'story_area'})
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
    content = content.strip()

    os.environ["NLS_LANG"] = ".AL32UTF8"
    START_VALUE = u"Unicode \u3042 3".encode('utf-8')
    END_VALUE = u"Unicode \u3042 6".encode('utf-8')

    conn = oc.connect('hyeminseo/hyeminseo@203.236.209.97:1521/XE')
    cursor = conn.cursor()
    cursor.execute('insert into movie values(:movie_no, :movie_title, :movie_titleEng, :movie_genre, :movie_nation, :movie_runtime, :movie_grade, :movie_opendate, :movie_director, :movie_actor, :movie_image_url, :movie_play_url, :movie_content, :movie_nowplaying, :movie_nowrank)',
                   movie_no=int(movino), movie_title=title, movie_titleEng=titleeng, movie_genre=genre, movie_nation=nation, movie_runtime=runtime, movie_grade=grade, movie_opendate=opendate,
                   movie_director=director, movie_actor=actor, movie_image_url=src, movie_play_url=play_url, movie_content=content, movie_nowplaying=1, movie_nowrank=null)
    conn.commit()
    cursor.close()
    conn.close

    no.append(int(movino))

print(no)
print(len(no))