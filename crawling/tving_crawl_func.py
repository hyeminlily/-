from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import requests
import re

def getTitleList():
    driver = webdriver.Chrome()
    driver.get("http://www.tving.com/movie/allm")
    time.sleep(10)

    # infinite scroll
    body = driver.find_element_by_tag_name("body")
    num_of_padedown = 1000

    while num_of_padedown:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(10)
        num_of_padedown -= 1

    # get movie's title from Tving
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    caption = soup.findAll('div', {'class': "caption"})

    title_list = []
    for c in caption:
        text = c.find('a').text
        text = text.replace("[할인] ", "")
        text = text.replace("[이벤트] ", "")
        text = text.replace(" [대여상품] ", "")
        text = text.replace(" [소장상품] ", "")
        text = text.replace(" [본편&코멘터리] ", "")
        text = text.replace(" [더빙]", "")
        text = text.replace(" [자막]", "")
        text = text.replace(" 무삭제", "")
        text = text.replace("확장판", "")
        title_list.append(text.strip())

    # get movie's title from Cinefox
    for page in range(234):
        url = 'http://clean.cinefox.com/vod/movie/list?page=' + str(page + 1)
        result = requests.get(url)
        data = BeautifulSoup(result.content, 'html.parser')
        div = data.findAll('div', {'class': "title"})
        for d in div:
            text = d.text
            title = re.sub('\t|\r|\n', '', text)
            title = title.replace(" 2D", "")
            title = title.replace(" 3D", "")
            title = title.replace(" [자막]", "")
            title = title.replace(" (더빙)", "")
            title = title.replace(" [더빙]", "")
            title = title.replace(" [1996]", "")
            title = title.replace(" [재개봉]", "")
            title = title.replace(" [극장판]", "")
            title = title.replace(" [특별판]", "")
            title = title.replace(" [요약판]", "")
            title = title.replace(" [완결판]", "")
            title = title.replace(" [확장판]", "")
            title = title.replace(" [무삭제]", "")
            title = title.replace(" [무삭제 특별판]", "")
            title = title.replace(" [무삭제 감독판]", "")
            title = title.replace(" [무삭제판]", "")
            title = title.replace("[무삭제판]", "")
            title = title.replace(" [리마스터링]", "")
            title = title.replace(" [리마스터링 재개봉]", "")
            title = title.replace(" [ 소장용 ]", "")
            title = title.replace(" [본편+메이킹필름]", "")
            title = title.replace(" [감독 확장판]", "")
            title = title.replace(" (감독판)", "")
            title = title.replace(" (극장판)", "")
            title = title.replace("(감독판)", "")
            title = title.replace("(극장판)", "")
            title = title.replace("(디오리지널)", "")
            title = title.replace("(리마스터링)", "")
            title = title.replace(" (청각장애인용 자막판)", "")
            title = title.replace(" 무삭제판", "")
            title = title.replace(" 무삭제 특별판", "")
            title = title.replace(" 무삭제 감독판", "")
            title_list.append(title)

    # remove overlapped title
    title_list = list(set(title_list))
    return title_list
