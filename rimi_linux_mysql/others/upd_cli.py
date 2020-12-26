import socket
pics = b''
ip = '127.0.0.1'
port = 19528
addr = (ip, port)
#tcp协议
ss = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
ss.connect(addr)
#python 调用系统底层
while True:
    data = input('data:')
    ss.send(data.encode('utf8'))
    data = ss.recv(1024)
    print(data)
