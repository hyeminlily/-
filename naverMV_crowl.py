from bs4 import BeautifulSoup
import requests
import re
import tving_crowl_func

list = tving_crowl_func.getTitleList()
for title in list:
    title = title.replace(" ", "+")

    # search in naver
    url = 'https://movie.naver.com/movie/search/result.nhn?query=' + title + "&section=all&ie=utf8"
    result = requests.get(url)
    html = BeautifulSoup(result.content, 'html.parser')
    ul = html.find('ul', {'class': "search_list_1"})
    no = ul.find('a')['href'].split("/")[-1].split("=")[-1]

    # get movie basic info (title, titleEng, genre, nation, runtime, opendate, age, content)
    url_mv = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=' + no
    result_mv = requests.get(url_mv)
    html_mv = BeautifulSoup(result_mv.content, 'html.parser')

    info = html_mv.find('div', {'class': "mv_info"})
    title = info.find('h3', {'class': "h_movie"}).find('a').text

    titleEng = info.find('strong', {'class': "h_movie2"}).text
    titleEng = re.sub('\t|\r|\n', '', titleEng)
    rm_year = re.findall('[0-9][0-9][0-9][0-9]', titleEng)
    titleEng = titleEng.replace(', ' + rm_year[0], '')
    titleEng = titleEng.replace(rm_year[0], '')

    info_spec = html_mv.find('dl', {'class': 'info_spec'})
    dd = info_spec.findAll('dd')

    genre = dd[0].findAll('span')[0].find('a').text
    nation = dd[0].findAll('span')[1].find('a').text
    runtime = dd[0].findAll('span')[2].text.strip()

    if len(dd[0].findAll('span')) > 3:
        year = dd[0].findAll('span')[3].findAll('a')
        split_year1 = str(year).split('>')
        split_year2 = split_year1[1].split('<')[0].strip()
        split_year3 = split_year1[3].split('<')[0]
        opendate = split_year2 + split_year3
        opendate = opendate.replace('.', '/')
    else:
        opendate = ''

    if len(dd) == 3:
        age = dd[2].find('a').text
    else:
        age = dd[3].find('a').text

    story_area = html_mv.find('div', {'class': 'story_area'})
    head = re.findall('<h5 class="h_tx_story">(.+?)</h5>', str(story_area))
    contents = re.findall('<p class="con_tx">(.+?)</p>', str(story_area))
    contents[0] = contents[0].replace('\r', '')
    contents[0] = contents[0].replace('\xa0', '')

    if len(head) != 0:
        content = head[0] + '<br/>' + contents[0]
    else:
        content = contents[0]

    # get movie detail info (director, actor)
    url_dt = 'https://movie.naver.com/movie/bi/mi/detail.nhn?code=' + no
    result_dt = requests.get(url_dt)
    html_dt = BeautifulSoup(result_dt.content, 'html.parser')

    directors = html_dt.find('div', {'class': "director"})
    directors_list = re.findall('<a class="k_name" href=".+?" title=".+?">(.+?)</a>', str(directors))
    director = ''
    for dir in directors_list:
        if dir == directors_list[-1]:
            director += dir
        else:
            director += dir + ', '

    actors = html_dt.find('div', {'class': "made_people"})
    actors_list = re.findall('<a class="k_name" href=".+?" title=".+?">(.+?)</a>', str(actors))
    actor = ''
    if len(actors_list) != 0:
        for act in actors_list:
            if act == actors_list[-1]:
                actor += act
            else:
                actor += act + ', '

    # get movie poster
    url_img = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + no
    result_img = requests.get(url_img)
    html_img = BeautifulSoup(result_img.content, 'html.parser')

    img_src = html_img.find('img', {'id': "targetImage"})['src']
    resource = requests.get(img_src)
    fname = no + '.jpg'
    img_file = 'C:/stsTest/2M_Project/src/main/webapp/resources/images/' + fname

    file = open(img_file, 'wb')
    file.write(resource.content)
    file.close()