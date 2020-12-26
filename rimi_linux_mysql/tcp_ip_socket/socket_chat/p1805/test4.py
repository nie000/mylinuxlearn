import queue
#pip install requests
import requests
from bs4 import BeautifulSoup
import threading


class Bole:
    def __init__(self):
        self.start_url = "http://python.jobbole.com/all-posts/"
        self.detail_tasks = queue.Queue()
        self.index_tasks = queue.Queue()
        #去重复的列表页面
        self.detail_list = []
        #在开始的时候加入到列表页面
        self.index_tasks.put(self.start_url)


    def get_html(self,url):
        """
        专门爬取页面的函数
        :param url:
        :return:
        """
        # print(url)
        r = requests.get(url)
        html = r.text
        # print(html)
        return html


    def get_detail(self):
        """
        获取到任务,并且把任务交给专门函数处理
        :return:
        """

        while True:

            url = self.detail_tasks.get()
            html = self.get_html(url)
            print('left detail tasks {}'.format(self.detail_tasks.qsize()))
            print('left index tasks {}'.format(self.index_tasks.qsize()))


    def get_index(self):
        """
        获取index的页面
        :return:
        """
        while True:

            url = self.index_tasks.get()
            html = self.get_html(url)
            detail_lists, index_lists = self.parse_index(html)
            for i in detail_lists:
                self.detail_tasks.put(i)
            for i in index_lists:
                #递归函数
                self.index_tasks.put(i)

    def parse_index(self,html):
        dom = BeautifulSoup(html)
        detail_dom = dom.find_all('a', class_='archive-title')
        index_dom = dom.find_all('a', class_='page-numbers')
        detail_lists = []
        index_lists = []
        for i in detail_dom:
            if i not in self.detail_list:
                detail_lists.append(i.attrs['href'])
                self.detail_list.append(i)

        for i in index_dom:
            index_lists.append(i.attrs['href'])

        return detail_lists,index_lists

    def test(self):
        html = self.get_html(self.start_url)
        dom = BeautifulSoup(html)
        detail_dom = dom.find_all('a', class_='archive-title')
        index_dom = dom.find_all('a', class_='page-numbers')
        detail_lists = []
        index_lists = []
        for i in detail_dom:
            detail_lists.append(i.attrs['href'])
        for i in index_dom:
            index_lists.append(i.attrs['href'])

        return detail_lists,index_lists

    def start(self):
        #
        # self.get_index(self.start_url)
        t1 = threading.Thread(target=self.get_index)
        t2 = threading.Thread(target=self.get_detail)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

if __name__ == "__main__":
    bole = Bole()
    bole.start()



# 1. 早上的socket
# 2. 爬取index页面 通过 http://blog.jobbole.com/all-posts/  把1-500页都爬出来
    # 1. 递归方式爬取
    # 2. 生成者消费者模型爬
    # 3. 两个方式的不同
# 3. 通过2把详情页面的a标签爬出来,放到一个任务里面, 另外一个函数取a标签,并且爬取a标签的页面




