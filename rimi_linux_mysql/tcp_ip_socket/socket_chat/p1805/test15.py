#1. 系统底层有 才能有使用

import select
import socket
# 1. 读  2.写  3.报错

# 1. read  2. write  3. 报错时间

ss = socket.socket()


ss.bind(('0.0.0.0',19529))
ss.listen()

readlist = [ss]
writelist = []
errorlist = []

msg_dict = {}
# select()

# def select(r,w,x):
#
#     return r1,w1,x1
# readlist = [ss,conn1,conn2,conn3]
while 1:
    #读事件,可能是ss server收到一个新的链接请求 也能是已经链接好的conn发送数据过来
    # rlist = []
    # wlist = [conn2]
    rlist, wlist, xlist = select.select(readlist, writelist, errorlist)
    #如果向下执行了,就说明发生了事件
    #if
    #需求  一问一答 但是可以有多人一问一答 没有广播
    #回调增加代码复杂度
    if rlist:
        for i in rlist:
            if i is ss:
                #这时候缓冲区非空 可以开始读取数据
                try:
                    conn, addr = i.accept()
                    readlist.append(conn)
                except Exception:
                    continue
            else:
                try:
                    #链接1
                    msg = i.recv(1024)
                    msg_dict[i] = msg
                    if not msg:
                        i.close()
                        readlist.remove(i)
                        continue
                    else:
                        #阻塞
                        # i.send(msg)
                        print(msg)
                        # readlist.remove(i)
                        writelist.append(i)
                except Exception:
                    i.close()
                    readlist.remove(i)
                    continue
    if wlist:
        for i in wlist:
            try:
                #链接1 准备发送数据
                msg = msg_dict[i]
                i.send(msg)
                del(msg_dict[i])
                writelist.remove(i)
                # readlist.append(i)
            except Exception:
                i.close()
                writelist.remove(i)


# ss.listen(5)
# conn,addr = ss.accept()
# msg = conn.recv(1024)
# conn.send(msg)