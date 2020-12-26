import socket
send_address = ("0.0.0.0",23456)
cli = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#直接连接
cli.connect(send_address)
#发送数据
cli.send(b'teset')
#接受数据
msg = cli.recv(1024)
print(msg)
cli.close()