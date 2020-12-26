import requests
from bs4 import BeautifulSoup
from threading import Thread
import time

num = 0
start_time = time.time()
#获取html
def get_html(url):
    r = requests.get(url)
    html = r.text
    count()
    a_list = parse_a(html)
    for i in a_list:
        # get_html(i)
        Thread(target=get_html,args=(i,)).start()
    return html

def parse_a(html):
    dom = BeautifulSoup(html)
    a_list = dom.find_all('span', class_='digg-item-updated-title')

    all_list = []
    for i in a_list:
        a = i.find('a')
        href = a.attrs.get('href', None)
        if href:
            all_list.append(href)

    return all_list

def logs(html):
    print(html)

def count():
    global num
    num += 1
    print('当前爬取了{}网页'.format(str(num)))

def count_time():
    global num
    global start_time
    print('开始计时')
    while True:
        if num >= 50:
            end_time = time.time()
            print("花费时间{}".format(str(end_time-start_time)))
            break



# def count_time_deamon():
#     while count_time():
#         return False



def start(url="http://python.jobbole.com/89290/"):
    get_html(url)
    # a_list = parse_a(html)
    # for i in a_list:
    #     start(i)

if __name__ == "__main__":
    # start()

    Thread(target=start).start()
    Thread(target=count_time).start()
