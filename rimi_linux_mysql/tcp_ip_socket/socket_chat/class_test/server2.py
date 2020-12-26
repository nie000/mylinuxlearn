import socket
import threading

#返回的是tuple

def return_msg(conn,addr):
    print('accept connections from',addr)
    #conn表示我和客户端的一个连接
    #一次接受多少个字节
    #send 只能发送二进制数据
    #msg是二进制
    while True:
        msg = conn.recv(1024)
        msg = msg.decode('utf8')
        if msg == "fin":
            conn.send(b'close connection')
            conn.close()
            break
        return_msg = 'accept your msg {}'.format(msg)
        # return_msg = input('return:')
        conn.send(return_msg.encode('utf8'))
        print(msg)
    print('connection closed')
    # #四次挥手 关闭连接

IP = '10.2.0.102'
PORT = 19522
address = (IP,PORT)
#AF_INET 使用ip协议 #SOCK_STREAM使用tcp协议
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(address)
server.listen(18)
while 1:
    conn, addr = server.accept()
    threading.Thread(target=return_msg,args=(conn,addr)).start()
