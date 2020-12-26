import socket
from concurrent.futures import ThreadPoolExecutor

class Client:

    def __init__(self,ip='127.0.0.1',port=20008):
        self.ip = ip
        self.port = port
        self.bind_ip = (ip, port)
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pools = ThreadPoolExecutor(5)

    def start(self):
        self.ss.connect(self.bind_ip)
        self.pools.submit(self.send)
        self.pools.submit(self.recv)


    def send(self):
        while True:
            msg = input('输入消息:')
            self.ss.send(msg.encode())
    def recv(self):
        while True:
            msg = self.ss.recv(1024)
            print('收到消息{}'.format(msg.decode()))


if __name__ == "__main__":
    c = Client()
    c.start()