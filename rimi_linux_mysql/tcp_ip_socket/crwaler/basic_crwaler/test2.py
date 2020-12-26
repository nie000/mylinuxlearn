import requests
from bs4 import BeautifulSoup

index_urls_list = []


def get_html_doc(url):
    # 根据指定的url获取html文档
    res = requests.get(url)
    print(res.content)
    return res.content.decode("utf8")


def parse_index(url):
    # 解析列表页面
    html_doc = get_html_doc(url)
    data = BeautifulSoup(html_doc)
    # 把index里面的url取出来再取下面的url
    # data.select调用css选择器 选择出来是dict
    detail_urls = data.select('[class=post-thumb] a')

    for i in detail_urls:
        url = i['href']
        get_html_doc(url)
    # 取出所有其他index页面的翻页url 去解析其他的url
    index_urls = data.select('a[class=page-numbers]')
    for i in index_urls:
        if i not in index_urls_list:
            index_urls_list.append(i)
            url = i['href']
            parse_index(url)


def start(url):
    parse_index(url)


if __name__ == "__main__":
    url = "http://blog.jobbole.com/category/it-tech/"
    start(url)
