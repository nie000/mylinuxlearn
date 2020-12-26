import socket
import select

r = []

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('127.0.0.1',28889))
server.listen(1)


r.append(server)

while True:
    rlist,wlist,xlist = select.select(r,[],[])
    for i in rlist:
        if i is server:
            con,add = i.accept()
            print(add)
            r.append(con)
        else:
            try:
                m = i.recv(1024)
                if not m:
                    i.close()
                    r.remove(i)
                    continue
            except:
                r.remove(i)