from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import cx_Oracle as oc
import os

def getGraph(no):
    # Oracle Connection
    os.environ["NLS_LANG"] = ".AL32UTF8"
    START_VALUE = u"Unicode \u3042 3".encode('utf-8')
    END_VALUE = u"Unicode \u3042 6".encode('utf-8')

    conn = oc.connect('hyeminseo/hyeminseo@localhost:1521/XE')
    cursor = conn.cursor()
    cursor.execute("select nvl(to_char(good_date, 'yyyy/mm/dd'), 'sum') good_date, count(*) cnt from good"
                   "where member_no = 2 group by rollup(to_char(good_date, 'yyyy/mm/dd'))")

    date = []
    cnt = []
    for cs in cursor:
        if cs[0] != 'sum':
            date.append(cs[0])
            cnt.append(cs[1])

    cursor.close()
    conn.close

    # matplot graph
    rc('font', family=font_manager.FontProperties(fname='C:/WINDOWS/Fonts/TmonMonsori.ttf.ttf').get_name())
    with plt.style.context('ggplot'):
        plt.plot(date, cnt, color='#68B4AB')
        plt.ylabel('좋아요 횟수', fontsize=16)
        plt.savefig(r'static/images/cnt_graph_' + str(no) + '.jpg', format='jpg')