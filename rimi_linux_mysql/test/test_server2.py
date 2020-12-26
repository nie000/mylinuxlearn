import socket
import select
import re

HOST = "localhost"
PORT = 9898
ADDR = (HOST, PORT)
BUFSIZE = 1024

_service_socket = socket.socket()
_service_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
_service_socket.bind(ADDR)
_service_socket.listen(10)

_current_in_list = [_service_socket]


#问题 io多路复用之间如何传递信息
def main():
    while True:
        rlist, wlist, xlist = select.select(_current_in_list, [], [])
        for i in rlist:
            if i is _service_socket:
                conn, addr = i.accept()
                _current_in_list.append(conn)

            else:
                msg = i.recv(1024)
                i.send(msg)


if __name__ == '__main__':
    main()
