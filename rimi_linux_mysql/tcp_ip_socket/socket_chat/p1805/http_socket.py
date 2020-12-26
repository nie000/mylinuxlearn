import socket

addr = ('www.zhihu.com', 80)
ss = socket.socket()
ss.connect(addr)
x = b"GET / HTTP/1.1\r\nHost: www.zhihu.com\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36\r\n"
x += b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"
x += b"Accept-Encoding: gzip, deflate\r\n"
x += b"Accept-Language: zh-CN,zh;q=0.9,en;q=0.8\r\n\r\n"
ss.send(x)
msg = ss.recv(1024 * 1024 * 10)
print('recv data')
print(msg.decode('utf8'))

