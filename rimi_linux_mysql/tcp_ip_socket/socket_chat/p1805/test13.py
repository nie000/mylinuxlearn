import socket
from concurrent.futures import ThreadPoolExecutor


class Client:

    def __init__(self, ip='0.0.0.0', port=21805):
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
            if (not msg) or len(msg) == 0:
                """
                当消息为空或者没有消息还发送过来的时候,断开链接
                """
                self.ss.close()
                break
            print('收到消息{}'.format(msg.decode()))
        print('链接已经断开')


if __name__ == "__main__":
    c = Client()
    c.start()
