import socket
from urllib import parse
from dns import resolver


# r = requests.get('http://blog.jobbole.com/114499/')

def req(url):
    i = parse.urlparse(url)
    host = i.hostname
    path = i.path
    header = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\r\n\r\n".format(
        path, host).encode('utf8')

    host_ip_list = resolver.query(host)
    host_ip = host_ip_list.response.answer[0].items[0].address
    ss = socket.socket()
    addr = (host_ip, 80)
    ss.connect(addr)
    ss.send(header)
    data = b""
    while 1:
        msg = ss.recv(10)
        if not msg:
            break
        data += msg
    data = data.split(b'\r\n\r\n')

    html_list = data[1:]
    html = b"".join(html_list)
    print(html.decode('utf8'))


r = req('http://blog.jobbole.com/114499/')
