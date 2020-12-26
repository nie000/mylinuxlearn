import socket
send_address = ("0.0.0.0",19527)
cli = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#直接连接
cli.connect(send_address)
#发送数据
cli.setblocking(False)

#接受数据

msg = cli.recv(1024)

for i in range(10000):
    print(i)

while True:
    msg = cli.recv(1024)
print(msg)
cli.close()