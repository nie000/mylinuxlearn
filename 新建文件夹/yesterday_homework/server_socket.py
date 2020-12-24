# 1、客户端发送两次消息，服务器端接收两次，然后服务器端返回一次消息。
# import socket
#
# # 申明
# ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 绑定地址和监听
# ss.bind(("127.0.0.1", 8001))
# ss.listen()
# # 获取客户端socket和地址
# cli, addr = ss.accept() #等待客户端连接
# # 获取tcp消息 一次1kb
# msg1 = cli.recv(1024)   #等待客户端发送消息
# print(msg1)
# msg2 = cli.recv(1024)   #等待客户端发送消息
# print(msg2)
# # 回送消息
# cli.send(b'get')
# ss.close()

# 2、可以使用中文通信。
# import socket
#
# # 申明
# ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 绑定地址和监听
# ss.bind(("127.0.0.1", 8001))
# ss.listen()
# # 获取客户端socket和地址
# cli, addr = ss.accept() #等待客户端连接
# # 获取tcp消息 一次1kb
# msg1 = cli.recv(1024)   #等待客户端发送消息
# print(msg1.decode(encoding='utf-8'))
# # 回送消息
# cli.send('收到'.encode(encoding='utf-8'))
# ss.close()

# 3、保持客户端与服务器一直存活，可以一个功能，客户端，发送小写字母，服务器返回大写字母，用户不断的输入，服务器不断的返回。
import socket

# 申明
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定地址和监听
ss.bind(("127.0.0.1", 8001))
ss.listen()
# 获取客户端socket和地址
cli, addr = ss.accept() #等待客户端连接
while True:
    # 获取tcp消息 一次1kb
    msg1 = cli.recv(1024).decode('utf-8')   #等待客户端发送消息
    print(msg1)
    upper_msg=msg1.upper()
    # 回送消息
    cli.send(upper_msg.encode(encoding='utf-8'))
ss.close()