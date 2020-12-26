#模拟爬虫爬去网站页面

import time
import threading

detail_url_list = []

def get_detail_html():
    global detail_url_list
    for url in detail_url_list:
        print("get detail html start")
        time.sleep(2)
        print("get detail html end")


def get_detail_url():
    global detail_url_list
    print('get detail url start')
    time.sleep(4)
    for i in range(20):
        detail_url_list.append("https://www.baidu.com/{}".format(i))
        print("get detail url end")


