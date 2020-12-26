import requests
from bs4 import BeautifulSoup
root_url = "http://blog.jobbole.com/all-posts/"

# r = requests.get(root_url)
# soup = BeautifulSoup(r.text)
#
# list_links = soup.select('a.archive-title')
# index_links = soup.select('a.page-numbers')
#
# for i in list_links:
#     tmp_href = i.attrs['href']
#     r = requests.get(tmp_href)
#     print(r.text)

record_list = []

def start():
    url = "http://blog.jobbole.com/all-posts/"
    record_list.append(url)
    html = get_html(url)
    soup = BeautifulSoup(html)
    #详情页面的a标签
    list_links = soup.select('a.archive-title')
    # parse_list(list_links)
    #列表的a标签
    index_links = soup.select('a.page-numbers')
    parse_index(index_links)

def parse_index(index_links):
    global record_list
    for i in index_links:
        #tmp_href是一个index的连接
        tmp_href = i.attrs['href']
        if tmp_href in record_list:
            continue
        record_list.append(tmp_href)
        html = get_html(tmp_href)
        #列表页的html
        index_soup = BeautifulSoup(html)
        # 详情页面的a标签
        list_links = index_soup.select('a.archive-title')
        parse_list(list_links)
        # 爬去列表页面
        index_links = index_soup.select('a.page-numbers')
        parse_index(index_links)


def parse_list(list_links):
    for i in list_links:
        tmp_href = i.attrs['href']
        res = get_html(tmp_href)
        print(res)


def get_html(url):
    r = requests.get(url)
    return r.text


if __name__ == '__main__':
    start()
