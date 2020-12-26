# python select io多路复用测试代码
# 1. 简单的使用select来进行客户端多连接

import select
import socket
import time

# select 把socket放入 select中,然后每当有一个连接过来,把连接conn放入select模型里面去

port = 19834
ip = "127.0.0.1"
time.sleep(5)
ss = socket.socket()
ss.bind((ip, port))
ss.listen(10)

readable_list = [ss]


while 1:
    # print('listen again')
    rlist, wlist, xlist = select.select(readable_list, [], [],5)
    # 如果遍历出来的
    print('listen to the readable sockets',rlist)
    print('length of the readable sockets',len(rlist))
    print('length of the total sockets', len(readable_list))
    for i in rlist:
        print('---------rlist--------------')
        if i is ss:
            print('---------ss--------------')
            #如果ss准备就绪,那么说明ss就可以接受连接了,当ss接受到连接
            #那么把连接返回readlist
            conn,addr = i.accept()
            readable_list.append(conn)
        #如果不是socket对象,那么就是conn连接对象了,如果是conn连接对象,那么就代表有
        #读入数据的变化,对应recv方法
