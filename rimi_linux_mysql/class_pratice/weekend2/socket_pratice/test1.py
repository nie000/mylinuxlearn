#socket
import socket
# 端口
ss = socket.socket()
#bind的某个端口 这个端口只负责收到链接请求
ss.bind(("127.0.0.1",8002))
ss.listen(10)
#80 相当于tcp层或者udp
print("ready to accept")
while True:
    #分配一个新的端口号进行数据交互
    conn, addr = ss.accept()
    msg = conn.recv(1024)
    print(msg)



