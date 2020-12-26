# 使用socket获取http报文
import socket
from urllib.parse import urlparse
from select import select,poll,kqueue
read_list = []
write_list = []
exec_list = []
#select 第一个list读数据,写数据,错误数据的io
# 初始化socket
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
domain = "https://www.baidu.com"
url = urlparse(domain)
host = url.netloc
path = url.path
if path == "":
    path = "/"
ss.bind(('0.0.0.0',29580))
# ss.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
ss.listen(10)
ss.setblocking(False)
read_list.append(ss)
while True:
    print('ok')
    rlist,wlist,xlist = select(read_list,write_list,exec_list)
    for i in rlist:
        if i is ss:
            #i相当于是ss
            #ss 是服务器准备好了
            #conn 是连接准备好了
            conn,addr = i.accept()
            read_list.append(conn)
        else:
            #i 相当于是 conn
            try:
                msg = i.recv(1024)
                print(msg)
            except Exception:
                read_list.remove(i)

