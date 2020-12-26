from bs4 import BeautifulSoup
import requests, queue, time
from threading import Thread


class Bole(object):
    def __init__(self):
        self.url_temp = "http://python.jobbole.com/all-posts/"
        self.n = 1
        self.url_list = [self.url_temp]

    def html_get(self):
        response = requests.get(self.url_temp)
        html = response.content.decode()
        # print(html)
        return html

    def get_page_url(self):
        html = self.html_get()
        url_all = BeautifulSoup(html)
        url_nextpage = url_all.find_all("a", attrs={"class": 'next page-numbers'})
        # print(url_nextpage)

        for i in url_nextpage:
            url_next = i.get('href')
            print(url_next)
            self.url_list.append(url_next)

        self.n += 1
        time.sleep(1)
        """
        不爬完 只爬取六次
        """
        if self.n <= 5:
            self.url_temp = url_next
            self.get_page_url()

    def prase_url(self):
        # for i in self.url_list:
        if self.url_list != []:
            response = requests.get(self.url_list.pop())
            html = response.content.decode()
            print(html)
            time.sleep(1)
            self.prase_url()


if __name__ == '__main__':
    bole = Bole()
    t1 = Thread(target=bole.get_page_url)
    t2 = Thread(target=bole.prase_url)
    t2.start()
    t1.start()
    t1.join()
    t2.join()
    print('--------------end------------------')
