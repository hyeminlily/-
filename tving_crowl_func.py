from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

def getTitleList():
    driver = webdriver.Chrome()
    driver.get("http://www.tving.com/movie/allm")
    time.sleep(1)

    # infinite scroll
    body = driver.find_element_by_tag_name("body")
    num_of_padedown = 1

    while num_of_padedown:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        num_of_padedown -= 1

    # get movie's title from tving
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    caption = soup.findAll('div', {'class': "caption"})

    title_list = []
    for c in caption:
        text = c.find('a').text
        text = text.replace("[이벤트] ", "")
        text = text.replace(" [자막]", "")
        title_list.append(text.strip())

    # print(len(title_list))
    # print(title_list)

    return title_list

# getTitleList()