import socket
addr = ('0.0.0.0',10003)
# socket链接对象 STREAM 数据流 使用ipv4通信

ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# upd  DGRAM upd
# unix通信 文件通信
# ss_d = socket.socket(socket.SOCK_DGRAM)
# upd,tcp
# 占用一个端口,ip 0.0.0.0 tuple
ss.bind(addr)
# 监听这个端口
ss.listen()
#等待链接过来
# conn是链接对象 address 是ip 端口号
#accept三次握手 ,建立链接 ---->conn
print('serve start')
conn,address = ss.accept()
print(conn)
print('---------------')
print(address)
# accept 在接收到链接之前 会一直阻塞 不会消耗cpu
#交换数据
conn.setblocking(False)
while 1:
    try:
        msg = conn.recv(1024)
    except Exception:
        pass
print(msg.decode("utf8"))
conn.close()
ss.close()
print('serve over')
