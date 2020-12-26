import requests
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread


def get_html_doc(url):
    # 根据指定的url获取html文档
    res = requests.get(url)
    print(res.content)
    return res.content.decode("utf8")


def get_detail(que):
    while True:
        url = que.get()
        Thread(target=get_html_doc, args=(url,))


def parse_index(url, que, index_urls_list):
    # 解析列表页面
    html_doc = get_html_doc(url)
    data = BeautifulSoup(html_doc)
    # 把index里面的url取出来再取下面的url
    # data.select调用css选择器 选择出来是dict
    detail_urls = data.select('[class=post-thumb] a')
    # 获取细节的url,把细节的url交给其他线程处理
    for i in detail_urls:
        que.append(i)
    # 取出所有其他index页面的翻页url 去解析其他的url
    index_urls = data.select('a[class=page-numbers]')
    for i in index_urls:
        # 保证不重复
        if i not in index_urls_list:
            index_urls_list.append(i)
            url = i['href']
            Thread(target=parse_index, args=(url, que))


def start(url, que, index_urls_list):
    parse_index(url, que, index_urls_list)


if __name__ == "__main__":
    url = "http://blog.jobbole.com/category/it-tech/"
    que = Queue()
    index_urls_list = Queue()

    start(url, que, index_urls_list)