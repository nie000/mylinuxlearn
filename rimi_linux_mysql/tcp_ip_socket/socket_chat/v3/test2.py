# 使用socket获取http报文
import socket
from urllib.parse import urlparse

# 初始化socket
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
domain = "https://www.baidu.com"
url = urlparse(domain)
host = url.netloc
path = url.path
if path == "":
    path = "/"
ss.connect((host, 80))
#'\r'的本意是回到行首，'\n'的本意是换行
data = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\r\n\r\n".format(
    path, host).encode('utf8')
ss.send(data)
res = b""
#报文就不像聊天数据那么小了 需要循环的拼接报文
while True:
    d = ss.recv(1024)
    if d:
        res += d
    else:
        break
print(res.decode('utf8'))
ss.close()