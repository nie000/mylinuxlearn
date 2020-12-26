"""
1. 生产者消费消费者模型爬取页面
2. 部件
     1. 队列去存储任务
     2. 去重
     3. 生产者
     4. 消费者
"""

import requests
import queue
from bs4 import BeautifulSoup
import threading
# currnet con
from concurrent.futures import ThreadPoolExecutor


class Bole:

    def __init__(self):
        # 启动爬虫的url
        self.start_url = 'http://python.jobbole.com/all-posts/'
        # 爬取index页面的任务列表
        self.index_tasks = queue.Queue()
        self.detail_tasks = queue.Queue()
        self.history = []
        self.detail_num = 0
        self.pools = ThreadPoolExecutor(5)

    def index_crawler(self):
        """
        爬取index页面
        :return:
        """
        while 1:
            # 如果没有任务 阻塞
            url = self.index_tasks.get()
            # threading.Thread(target=self.get_html,args=(url,)).start()
            html = self.get_index_html(url)
            self.parse_index(html)

    def detail_crawler(self):
        """
        爬取detail页面
        :return:
        """
        while 1:
            # 如果没有任务 阻塞
            url = self.detail_tasks.get()
            # threading.Thread(target=self.get_detail_html,args=(url,)).start()
            self.pools.submit(self.get_detail_html, url)
            # self.get_detail_html(url)
            self.detail_num += 1
            # print('当前爬取了{}个详情页面'.format(self.detail_num))
            print('剩余{}个detail页面的任务'.format(self.detail_tasks.qsize()))
            # TODO 以后把这个html入库

    def get_detail_html(self, url):
        r = requests.get(url)
        return r.text

    def get_index_html(self, url):
        if url not in self.history:
            r = requests.get(url)
            self.history.append(url)
            # print('已经爬取了{}个index页面'.format(len(self.history)))
            print('剩余{}个index页面的任务'.format(self.index_tasks.qsize()))
            return r.text
            # self.parse_index(r.text)
        else:
            return ""

    def parse_index(self, html):
        """
        专门解析index页面 并且把Index页面的下一页url找出来
        :param html:
        :return:
        """
        try:
            url_all = BeautifulSoup(html)

            # 布置Index页面的任务
            next_urls = url_all.find_all("a", attrs={"class": 'next page-numbers'})
            for i in next_urls:
                next_url = i.get('href')
                self.index_tasks.put(next_url)

            # 布置详情页面的任务
            a_list = url_all.find_all('a', class_='archive-title')
            for i in a_list:
                href = i.get('href')
                self.detail_tasks.put(href)

        except Exception:
            pass

    def start(self):
        self.index_tasks.put(self.start_url)
        # c1 = threading.Thread(target=self.index_crawler)
        # c2 = threading.Thread(target=self.detail_crawler)
        # c1.start()
        # c2.start()
        # c1.join()
        # c2.join()
        self.pools.submit(self.index_crawler)
        self.pools.submit(self.detail_crawler)


if __name__ == '__main__':
    bole = Bole()
    bole.start()
