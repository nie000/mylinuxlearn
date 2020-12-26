import socket
ip='127.0.0.1'
port=19528
addr = (ip,port)
#tcp协议
ss = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
ss.bind(addr)
while True:
    data,addr = ss.recvfrom(1024)
    ss.sendto(data,addr)