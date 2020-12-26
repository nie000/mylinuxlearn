#socket
import socket
# 端口
ss = socket.socket()
path = ""
host = "125.64.102.187"
ss.connect((host,80))
#http协议
#一问一答 一问一答
data = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\r\n\r\n".format(
    path, host).encode('utf8')
ss.send(data)
msg = ss.recv(1024)
print(msg)
print('all over')