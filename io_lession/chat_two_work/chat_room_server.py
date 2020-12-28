import socket
import threading



def chat_fun(cli,chat_list):
    while True:
        msg = cli.recv(1024)  # 阻塞
        for obj in chat_list:
            obj.send(msg)

if __name__ == '__main__':
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('127.0.0.1',8001))
    server.listen()
    chat_list=[]
    while True:
        cli,address=server.accept()  #阻塞
        chat_list.append(cli)
        threading.Thread(target=chat_fun, args=(cli,chat_list)).start()
