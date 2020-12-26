import socket
bind_address = ("0.0.0.0",19527)
#申明
ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#绑定地址和监听
ss.bind(bind_address)
ss.listen()
ss.setblocking(False)
#获取客户端socket和地址
cli,addr = ss.accept()
#获取tcp消息 一次1kb
msg = cli.recv(1024)
print(msg)
#回送消息
cli.send(b'get')
ss.close()
