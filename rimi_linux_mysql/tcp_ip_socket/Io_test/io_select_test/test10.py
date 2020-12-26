import socket
from urllib import parse
import select


class Crawler:

    def __init__(self):
        self.read_list = list()
        self.write_list = list()
        self.header_dict = dict()
        self.msg_dict = dict()
        self.stop = False

    def loop(self):
        while not self.stop:
            try:
                # windows如果select中三个list都是空会报错
                rlist, wlist, xlist = select.select(self.read_list, self.write_list, [])
            except OSError:
                continue
            for i in rlist:
                if i not in self.msg_dict.keys():
                    self.msg_dict[i] = b""
                try:
                    data = i.recv(1024)
                    if not data:
                        print(self.msg_dict[i])
                        del (self.msg_dict[i])
                        self.read_list.remove(i)
                    self.msg_dict[i] += data
                except Exception:
                    if i in self.msg_dict.keys():
                        del (self.msg_dict[i])
                    try:
                        self.read_list.remove(i)
                    except Exception:
                        pass

            for i in wlist:
                i.send(self.header_dict[i])
                self.write_list.remove(i)
                self.read_list.append(i)

    def add_task(self, url):
        if isinstance(url, list):
            for i in url:
                self.do_task(i)
        else:
            self.do_task(url)

    def do_task(self, url):
        header = self.gen_header(url)
        host, _ = self.parse_url(url)
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.connect((host, 80))
        ss.setblocking(False)
        # 文件描述符 1 2 3 4 5 6 7
        self.write_list.append(ss)
        self.header_dict[ss] = header
        # ss.send(header)
        # msg = ss.recv(1024)
        # print(msg)

    def parse_url(self, url):
        url_dict = parse.urlparse(url)
        host = url_dict.hostname
        path = url_dict.path
        if len(path) == 0:
            path = "/"
        return host, path

    def gen_header(self, url):
        # https://gitee.com/moist-master/rimi_linux_mysql
        host, path = self.parse_url(url)
        data = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497" \
               ".100 Safari/537.36\r\n\r\n".format(
            path, host).encode('utf8')
        return data

    def stop(self):
        self.stop = True


if __name__ == '__main__':
    url = "http://blog.jobbole.com/1142{}/"
    crawler = Crawler()
    url_list = list()
    for i in range(100):
        tmp_url = url.format(i)
        url_list.append(tmp_url)

    crawler.add_task(url_list)
    crawler.loop()
