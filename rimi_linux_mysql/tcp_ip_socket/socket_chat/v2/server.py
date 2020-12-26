import socket

ss_address = ("0.0.0.0",19534)
ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(ss_address)
ss.listen(2)
while True:
    #获取连接
    cli,addr = ss.accept()
    print('收到来自ip为{}的连接'.format(addr))
    #在连接的时候,进入循环
    while True:
        # 接受消息
        data = cli.recv(1024)
        if not data:
            break
        re_msg = "收到你的消息{}".format(data.decode('utf8'))
        cli.send(re_msg.encode('utf8'))
    cli.close()