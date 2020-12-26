import socket
import select

ss = socket.socket()

ss.bind(('127.0.0.1',19527))

ss.listen(5)

#读事件, 等待缓冲区由空变为非空 ss

# conn,addr = ss.accept()

# while 1:
#     msg = conn.recv()
#     conn.send(msg)


#select 轮询每一个事件,一旦事件有改变,告诉我们这个事件已经有改变
#select 监听 读 写 错误 事件
sel = select.select

readlist = [ss]
writelist = []
errorlist = []

while 1:
    #[ss]
    rlist,wlist,xlist = sel(readlist,writelist,errorlist)
    if rlist:
        for i in rlist:
            if i is ss:
                conn,addr = i.accept()
                readlist.append(conn)
            else:
                msg = i.recv(1024)
                writelist.append(i)
    if wlist:
        # [1,2,4,5]
        for i in wlist:
            i.send(b'hello')
            wlist.remove(i)



