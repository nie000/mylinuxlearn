import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


class MySocket:

    def get_conn(self):
        self.sel = DefaultSelector()
        self.host_port = ('0.0.0.0', 45633)
        self.ss = socket.socket()
        self.ss.setblocking(False)
        self.ss.bind(self.host_port)
        self.ss.listen(10)
        self.sel.register(self.ss.fileno(), EVENT_READ, self.get_accept)
        while 1:
            ready = self.sel.select()
            for key, mask in ready:
                print(key.data)
                call_back = key.data
                call_back(key)

    def get_accept(self, mask):
        self.sel.unregister(mask.fd)
        self.conn, self.addr = self.ss.accept()
        self.conn.setblocking(False)
        self.sel.register(self.conn.fileno(), EVENT_READ, self.get_recv)

    def get_recv(self, mask):

        # self.sel.unregister(mask.fd)
        self.data = self.conn.recv(1024)
        if self.data:
            # self.conn.send(self.data)
            self.sel.unregister(mask.fd)
            self.sel.register(self.conn.fileno(), EVENT_WRITE, self.get_send)
        else:
            self.conn.close()
            self.sel.unregister(mask.fd)

    def get_send(self, mask):
        self.sel.unregister(mask.fd)
        self.conn.send(self.data)
        self.sel.register(self.conn.fileno(), EVENT_READ, self.get_recv)


if __name__ == '__main__':
    my_socket = MySocket()
    my_socket.get_conn()
