import socket
import threading


def chat_fun(cli):
    while True:
        msg=cli.recv(1024)
        upder_msg=msg.decode('utf-8').upper()
        cli.send(upder_msg.encode('utf-8'))
if __name__ == '__main__':
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('127.0.0.1',8001))
    server.listen()
    while True:
        cli,address=server.accept()
        threading.Thread(target=chat_fun,args=(cli,)).start()
