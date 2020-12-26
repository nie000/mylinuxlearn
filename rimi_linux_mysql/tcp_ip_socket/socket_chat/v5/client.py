import socket

ss_address = ("0.0.0.0",19534)

ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ss.connect(ss_address)

while True:
    data = input('请输入消息:')
    if not data:
        break
    ss.send(data.encode('utf8'))
    print(ss.recv(1024).decode('utf8'))


ss.close()

