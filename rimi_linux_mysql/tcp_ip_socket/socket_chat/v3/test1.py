import socket
#使用tcp连接
ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.connect(('www.baidu.com',80))
print('connected')

# data = "GET / HTTP/1.1\r\nHost: www.baidu.com\r\n" \
#        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"

# data = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\r\n\r\n".format(
#     '/moist-master/rimi_linux_mysql/blob/master/tcp_ip_socket/notes/http_proto.md', 'www.baidu.com').encode('utf8')
# ss.send(data)


data = "POST {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\r\n\r\nspm=a21bo.2017.201867-main.30.5af911d96SRQjN&wh_weex=true&psId=1282014&wx_navbar_transparent=true&data_prefetch=true\r\n\r\n".format(
    '/moist-master/rimi_linux_mysql/blob/master/tcp_ip_socket/notes/http_proto.md', 'www.baidu.com').encode('utf8')
ss.send(data)
print('sended')

#每次就接受1kb
res = b""
while True:
    tmp_msg = ss.recv(1024)
    res += tmp_msg
    if not tmp_msg:
        break

print('recved')
print(res.decode('utf8'))

