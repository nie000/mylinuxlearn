import socket
import select
import sys
ss_address = ("0.0.0.0",19528)
ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.connect(ss_address)
#sys.stdin 系统的标准输入(键盘输入)
read_list=[ss,sys.stdin]
write_list = []
msg = []
while True:
    rlist,wlist,xlist = select.select(read_list,write_list,[])
    for i in rlist:
        if i is ss:
            data = i.recv(1024)
            if not data:
                break
            print(data.decode('utf8')+"\r\n")
        else:
            data = input('请输入:')
            if not data:
                if not data:
                    break
            print('\r\n')
            ss.send(data.encode('utf8'))





ss.close()

