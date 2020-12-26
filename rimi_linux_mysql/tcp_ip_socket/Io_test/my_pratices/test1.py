import select
import socket

address = ('0.0.0.0',19523)

ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(address)
ss.listen(5)
ss.setblocking(False)

read_list,write_list,ex_list = [ss],[],[]


msg_dict = dict()
while 1:
    rlist,wlist,xlist = select.select(read_list,write_list,ex_list)
    print('new loop')
    for i in rlist:
        if i is ss:
            #表示去接受一个连接请求
            conn,addr = i.accept()
            print('conn accept from {}'.format(addr))
            read_list.append(conn)
        else:
            print('conn recv---->')
            #如果请求过来的话 就去读取请求
            msg = i.recv(1024)
            #读取完请求后去回送数据
            #发送数据
            msg_dict.update({i:msg})
            write_list.append(i)

    for i in wlist:
        i.send(msg_dict[i])
        del(msg_dict[i])
        write_list.remove(i)

