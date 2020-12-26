import socket

ss_address = ("0.0.0.0",19528)

ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('123')
ss.connect(ss_address)
print('456')

while True:
    data = input('请输入消息:')
    if not data:
        break
    try:
        ss.send(data.encode('utf8'))
        print(ss.recv(1024).decode('utf8'))
    except BrokenPipeError:
        print('连接已经关闭')
        break


ss.close()

