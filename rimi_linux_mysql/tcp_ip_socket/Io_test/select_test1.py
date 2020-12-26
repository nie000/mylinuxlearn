# 使用socket获取http报文
# 把setblocking设为false 让学员自己解决问题
import socket
from urllib.parse import urlparse
from selectors import DefaultSelector


class Downloader:

    def __init__(self):
        self.domain = ""
        self.url = ""
        self.path = ""
        self.host = ""

    def get_connection(self):
        # 初始化socket

        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 使用非阻塞io，socket不等待连接建立好 直接向下执行
        self.ss.setblocking(False)
        # 只有一直try获取连接,因为连接还没有准备好
        while True:
            try:
                self.ss.connect((self.host, 80))
            except BlockingIOError as e:
                pass
            except OSError:
                break
        # 返回连接文件
        return self.ss

    def get_http(self):
        # '\r'的本意是回到行首，'\n'的本意是换行
        data = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\r\n\r\n".format(
            self.path, self.host).encode('utf8')
        self.ss.send(data)
        res = b""
        # 报文就不像聊天数据那么小了 需要循环的拼接报文
        # 让系统不断遍历 获取到recv因为不是阻塞的
        while True:
            try:
                d = self.ss.recv(1024)
            except BlockingIOError:
                continue
            if d:
                res += d
            else:
                break
        print(res.decode('utf8'))

    def get_html(self, domain="http://10.2.4.43:8000/detail/index/"):

        self.domain = domain
        self.url = urlparse(self.domain)
        self.host = self.url.netloc
        self.path = self.url.path
        if self.path == "":
            self.path = "/"

        self.get_connection()
        self.get_http()

        self.ss.close()


x = Downloader()
x.get_html()
