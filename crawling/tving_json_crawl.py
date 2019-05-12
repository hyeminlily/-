from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import re
import json

def getMovieList():

    # get json from Tving
    url = 'http://api.tving.com/v1/media/movies?pageSize=1000000000&order=new&free=all&adult=all&guest=all&scope=all&notMovieCode=M000227934%2CM000227739%2CM000228333%2CM000226839%2CM000226033%2CM000224433&personal=N&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610&_=1555906855903'
    rq = Request(url)
    rs = urlopen(rq)
    data = rs.read().decode('utf-8')
    getJson = json.loads(data)

    body = getJson["body"]
    result = body["result"]
    for r in result:

        # get detail json
        vod_code = r["vod_code"]
        url_dt = 'http://api.tving.com/v1/media/stream/info?apiKey=1e7952d0917d6aab1f0293a063697610&info=Y&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&mediaCode=' + vod_code + '&screenCode=CSSD0100&noCache=1555912726&callingFrom=HTML5&deviceId=3826034269&adReq=none&ooc='
        rq_dt = Request(url_dt)
        rs_dt = urlopen(rq_dt)
        data_dt = rs_dt.read().decode('utf-8')
        getJson_dt = json.loads(data_dt)

        body_dt = getJson_dt["body"]
        content = body_dt["content"]
        info = content["info"]

        # get title, titleEng
        vod_name = info["vod_name"]
        title = vod_name["ko"]
        title = title.replace("[이벤트]", "")
        titleEng = vod_name["en"]

        grade = info["grade_code"]
        print(grade)

        play_url = 'https://www.tving.com/movie/player/' + vod_code

        image_url = 'http://image.tving.com/resize.php?u=http://image.tving.com/upload/cms/caim/CAIM2100/' + vod_code + '.png&w=186'

getMovieList()
    # # get movie's title from Cinefox
    # for page in range(234):
    #     url = 'http://clean.cinefox.com/vod/movie/list?page=' + str(page + 1)
    #     result = requests.get(url)
    #     data = BeautifulSoup(result.content, 'html.parser')
    #     div = data.findAll('div', {'class': "title"})
    #     for d in div:
    #         text = d.text
    #         title = re.sub('\t|\r|\n', '', text)
    #         title = title.replace(" 2D", "")
    #         title = title.replace(" 3D", "")
    #         title = title.replace(" [자막]", "")
    #         title = title.replace(" (더빙)", "")
    #         title = title.replace(" [더빙]", "")
    #         title = title.replace(" [1996]", "")
    #         title = title.replace(" [재개봉]", "")
    #         title = title.replace(" [극장판]", "")
    #         title = title.replace(" [특별판]", "")
    #         title = title.replace(" [요약판]", "")
    #         title = title.replace(" [완결판]", "")
    #         title = title.replace(" [확장판]", "")
    #         title = title.replace(" [무삭제]", "")
    #         title = title.replace(" [무삭제 특별판]", "")
    #         title = title.replace(" [무삭제 감독판]", "")
    #         title = title.replace(" [무삭제판]", "")
    #         title = title.replace("[무삭제판]", "")
    #         title = title.replace(" [리마스터링]", "")
    #         title = title.replace(" [리마스터링 재개봉]", "")
    #         title = title.replace(" [ 소장용 ]", "")
    #         title = title.replace(" [본편+메이킹필름]", "")
    #         title = title.replace(" [감독 확장판]", "")
    #         title = title.replace(" (감독판)", "")
    #         title = title.replace(" (극장판)", "")
    #         title = title.replace("(감독판)", "")
    #         title = title.replace("(극장판)", "")
    #         title = title.replace("(디오리지널)", "")
    #         title = title.replace("(리마스터링)", "")
    #         title = title.replace(" (청각장애인용 자막판)", "")
    #         title = title.replace(" 무삭제판", "")
    #         title = title.replace(" 무삭제 특별판", "")
    #         title = title.replace(" 무삭제 감독판", "")
    #         title_list.append(title)
    #
    # # remove overlapped title
    # title_list = list(set(title_list))
    # return title_list
