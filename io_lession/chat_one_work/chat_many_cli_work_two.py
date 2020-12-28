import socket
import time

cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 直接连接
cli.connect(("127.0.0.1", 8001))
while True:
    content=input('请输入内容')
    # 发送数据
    cli.send(content.encode(encoding='utf-8'))
    # 接受数据
    msg = cli.recv(1024)
    print(msg.decode(encoding='utf-8'))
cli.close()