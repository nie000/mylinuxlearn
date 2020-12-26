import requests
from bs4 import BeautifulSoup
import queue
import threading

lock = threading.RLock()

index_urls_list = []


def get_html_doc(url):
    # 根据指定的url获取html文档
    # queue是线程安全的
    res = requests.get(url)
    # print(res.content)
    return res.content.decode("utf8")


def prase_detail(detail_tasks):
    while True:
        # tasks如果为空报错 阻塞 不会消耗cpu
        tmp_url = detail_tasks.get()
        # 详情页面
        res = get_html_doc(tmp_url)
        print('还有{}个获取详情页面的任务'.format(detail_tasks.qsize()))
        # print(res)


def index(index_tasks, detail_tasks):
    while True:
        tmp_url = index_tasks.get()
        # res就是我们的列表页面
        res = get_html_doc(tmp_url)
        try:
            data = BeautifulSoup(res)
        except Exception:
            continue
        detail_urls = data.select('[class=post-thumb] a')
        for i in detail_urls:
            # 详情页面的url
            url = i['href']
            # get_html_doc(url)
            # tasks的数据结构 list queue
            detail_tasks.put(url)
        index_urls = data.select('a[class=page-numbers]')
        for i in index_urls:
            if i not in index_urls_list:
                lock.acquire()
                index_urls_list.append(i)
                lock.release()
                url = i['href']
                index_tasks.put(url)
                print('还有{}个获取列表页面的任务'.format(index_tasks.qsize()))


if __name__ == "__main__":
    index_tasks = queue.Queue()
    detail_tasks = queue.Queue()
    url = "http://blog.jobbole.com/all-posts/"
    index_tasks.put(url)
    t1 = threading.Thread(target=index, args=(index_tasks, detail_tasks))
    tasks_list = [threading.Thread(target=prase_detail, args=(detail_tasks,)) for i in range(20)]
    t1.start()
    for i in tasks_list:
        i.start()
    t1.join()
    for i in tasks_list:
        i.join()
