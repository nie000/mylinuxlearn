import socket
import threading
import time




def chat_fun(cli):
    while True:
        msg = cli.recv(1024)
        print(msg.decode(encoding='utf-8'))
if __name__ == '__main__':
    name='张三:'
    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 直接连接
    cli.connect(("127.0.0.1", 8001))
    while True:
        threading.Thread(target=chat_fun, args=(cli, )).start()
        content=input('请输入内容')   #阻塞
        content=name+content
        # 发送数据
        cli.send(content.encode(encoding='utf-8'))



