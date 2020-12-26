import socket
from urllib import parse
from dns import resolver
def req(host):
    url = parse.urlparse(host)
    hostname = url.hostname
    path = url.path if url.path else '/'
    ss = socket.socket()
    res = resolver.query(hostname)
    i = res.response.answer[0][0]
    addr = (i.address, 80)
    ss.connect(addr)
    # header = "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36\r\n"
    # header += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n"
    # header += "Accept-Encoding: gzip, deflate\r\n"
    # header += "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8\r\n\r\n"
    header = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\r\n\r\n".format(
        path, hostname).encode('utf8')
    # header.format(path,hostname)
    ss.send(header)
    data = b""
    while True:
        msg = ss.recv(10)
        if not msg:
            break
        data +=msg
    # print('recv data')
    # print(data)
    data_list = data.split(b'\r\n\r\n')
    html_list = data_list[1:]
    html = b"".join(html_list)
    # return html.decode('utf8')
    print(html)

x = req('http://blog.jobbole.com/114499/')

print(x)