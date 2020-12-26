# if not None:
#     print('1515')

import socket
from urllib import parse
import select
import time

import requests  # 同步编程


# socket
class Crwaler:

    def __init__(self):
        # 初始化socket
        # self.ss = socket.socket()
        # self.ss.connect(("123.206.1.112", 80))
        # self.ss.setblocking(False)
        self.header = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:keep-alive\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\r\n\r\n"
        self.sec = select.select
        self.readlist = []
        self.writelist = []
        self.errorlist = []
        self.url_lists = []
        self.socket2host = dict()
        self.count = 0
        self.time = time.time()
        #1. 先关闭 再链接
        #2. 一次性线连接完,如果有 100个页面 那么先链接100个， 先new出100个socket来


    def add_url(self):
        for i in range(114000, 114600):
            tmp_url = "http://blog.jobbole.com/{}/".format(114461)
            self.url_lists.append(tmp_url)
            ss = socket.socket()
            ss.setblocking(False)
            try:
                ss.connect(("123.206.1.112", 80))
            except Exception:
                pass
            self.socket2host[ss] = tmp_url
            self.writelist.append(ss)


    def start(self):
        self.add_url()
        print('start--------')
        #每次可读了 但是读出来都是空事件
        while 1:
            r, w, e = self.sec(self.readlist, self.writelist, self.errorlist)
            if r:
                for i in r:
                    # print('read')
                    # # msg = b""
                    msg = i.recv(1024)
                    self.count += 1
                    print('已经爬取了{}页面'.format(self.count))
                    print('花费时间{}'.format(str(time.time()-self.time)))
                    print(msg)
                    self.readlist.remove(i)
                    i.close()
            if w:
                for i in w:
                    # print('write')
                    try:
                        # host = self.url_lists.pop()
                        host = self.socket2host[i]
                        # print(host)
                        # i.connect(("123.206.1.112", 80))
                        header, host = self.format_header(host=host)
                        try:

                            i.send(header.encode())
                            self.writelist.remove(i)
                            self.readlist.append(i)
                        except OSError:
                            i.connect(("123.206.1.112", 80))
                    except Exception as e:
                        self.writelist.remove(i)
                        continue

        print('end--------')




    def format_header(self, host):
        """
        帮助我们封装好报文
        :param host:
        :return:
        """
        url = parse.urlparse(host)
        hostname = url.hostname
        path = url.path if url.path else '/'
        header = self.header.format(path, hostname)
        return header, host

    def get_html(self, url):
        header, host = self.format_header(url)
        self.ss.connect(("123.206.1.112", 80))
        self.ss.send(header.encode())
        msg = b""
        while True:
            tmp_msg = self.ss.recv(1024)
            if not tmp_msg:
                break
            msg += tmp_msg

        print(msg)


if __name__ == "__main__":
    c = Crwaler()
    c.start()
