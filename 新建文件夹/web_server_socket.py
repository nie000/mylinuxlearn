import socket

# 申明
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定地址和监听
ss.bind(("127.0.0.1", 8002))
ss.listen()
while True:
    # 获取客户端socket和地址
    cli, addr = ss.accept() #等待客户端连接
    # 获取tcp消息 一次1kb
    msg1 = cli.recv(1024)   #等待客户端发送消息
    print(msg1.decode(encoding='utf-8'))
    # 回送消息
    data=b"""HTTP/1.1 200 OK\r\nConnection: keep-alive\r\n\r\n<h1>hello world!</h1>"""
    cli.send(data)
    ss.close()