import requests
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread
from concurrent.futures import ThreadPoolExecutor


def get_html_doc(url):
    # 根据指定的url获取html文档
    res = requests.get(url)
    print('ex--->url',url)
    return res.content.decode("utf8")


def get_detail(detail_urls_queue,pools):
    while True:
        url = detail_urls_queue.get(1,timeout=2)
        # print('consumer--->',url)
        pools.submit(get_html_doc,(url))


def parse_index(detail_urls_queue,index_urls_queue):
    while True:
        url = index_urls_queue.get(1)
        # print('get_index_url--->',url)
        # 解析列表页面
        html_doc = get_html_doc(url)
        data = BeautifulSoup(html_doc)

        # 把index里面的url取出来再取下面的url
        # data.select调用css选择器 选择出来是dict
        detail_urls = data.select('[class=post-thumb] a')
        # 获取细节的url,把细节的url交给其他线程处理
        for i in detail_urls:
            url = i['href']
            # print('productor------>',url)
            detail_urls_queue.put(url)



        # 取出所有其他index页面的翻页url 去解析其他的url
        index_urls = data.select('a[class=page-numbers]')
        for i in index_urls:
            url = i['href']
            index_urls_queue.put(url)
            #去重 使用redis数据库
            # print('put_index_url--->', url)


if __name__ == "__main__":
    url = "http://blog.jobbole.com/category/it-tech/"
    # 详细页面的url
    detail_urls = Queue()
    index_urls_queue = Queue()
    index_urls_queue.put(url)
    # 列表url 防止重复
    # index_urls_list = []
    executor = ThreadPoolExecutor(max_workers=10)
    t1 = Thread(target=parse_index,args=(detail_urls,index_urls_queue))
    t2 = Thread(target=get_detail, args=(detail_urls,executor))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('down')
