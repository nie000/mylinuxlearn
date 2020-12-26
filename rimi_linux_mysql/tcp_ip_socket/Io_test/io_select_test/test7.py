import socket

cli = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cli.connect(('0.0.0.0',13029))

while True:
    try:
        data = input('请输入:')
        cli.send(data.encode('utf8'))
        msg = cli.recv(1024)
        print(msg.decode('utf8'))
    except Exception:
        cli.close()
        break

print('会话已经结束')