import socket
import threading

class Cli:
    def __init__(self):
        self.addr = ('127.0.0.1',8008)
        self.ss = socket.socket()



    def recv(self):
        while True:
            msg = self.ss.recv(1024)
            print(msg.decode('utf8'))


    def send(self):
        while True:
            msg = input('put---:')
            self.ss.send(msg.encode('utf8'))



    def start(self):
        self.ss.connect(self.addr)

        t1 = threading.Thread(target=self.recv)
        t2 = threading.Thread(target=self.send)

        t1.start()
        t2.start()

        t1.join()
        t2.join()


if __name__ == "__main__":
    c = Cli()
    c.start()


