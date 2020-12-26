# --<!--utf8-->
import socket
# 0.0.0.0 = 内网网址
addr = ('127.0.0.1', 10041)
ss = socket.socket()
ss.connect(addr)
# while True:
#     msg = input('请输入:')
#     msg += '>'
#     ss.send(msg.encode('utf8'))
#     print('waiting recv')
#     recv_msg = ss.recv(1024)
#     print('recv msg')
#     print(recv_msg.decode('utf8'))


# id = 510104198901031
#
# id2 = "51010251511155"
#用户是用md5加密 把123456的用户的密码取出来
def md5():
    pass

pwd = '123456'

pwd = md5(pwd)

select * from user where pwd = pwd
