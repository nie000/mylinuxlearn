# 1、客户端发送两次消息，服务器端接收两次，然后服务器端返回一次消息。
# import socket
# import time
#
# cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 直接连接
# cli.connect(("127.0.0.1", 8001))
# # 发送数据
# cli.send(b'teset1')
# time.sleep(1)
# cli.send(b'teset2')
# # 接受数据
# msg = cli.recv(1024)
# print(msg)
# cli.close()

# 2、可以使用中文通信。
# import socket
# import time
#
# cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 直接连接
# cli.connect(("127.0.0.1", 8001))
# # 发送数据
# cli.send('传输中文'.encode(encoding='utf-8'))
# # 接受数据
# msg = cli.recv(1024)
# print(msg.decode(encoding='utf-8'))
# cli.close()

# 3、保持客户端与服务器一直存活，可以一个功能，客户端，发送小写字母，服务器返回大写字母，用户不断的输入，服务器不断的返回。
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