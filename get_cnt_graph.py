from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import cx_Oracle as oc
import os

def getGraph(no):
    # Oracle Connection
    os.environ["NLS_LANG"] = ".AL32UTF8"
    START_VALUE = u"Unicode \u3042 3".encode('utf-8')
    END_VALUE = u"Unicode \u3042 6".encode('utf-8')

    conn = oc.connect('hyeminseo/hyeminseo@203.236.209.97:1521/XE')
    cursor = conn.cursor()
    cursor.execute('select good_date, count(good_date) cnt from good where member_no = ' + str(no) + ' group by good_date order by good_date')

    date = []
    cnt = []
    for cs in cursor:
        date.append(cs[0].strftime("%Y/%m/%d"))
        cnt.append(cs[1])

    cursor.close()
    conn.close

    # matplot graph
    rc('font', family=font_manager.FontProperties(fname='C:/WINDOWS/Fonts/TmonMonsori.ttf.ttf').get_name())
    with plt.style.context('ggplot'):
        plt.plot(date, cnt, color='#68B4AB')
        plt.ylabel('좋아요 횟수', fontsize=16)
        plt.savefig(r'static/images/cnt_graph_' + str(no) + '.jpg', format='jpg')
