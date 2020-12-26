import socket
import os
ip='127.0.0.1'
port=19527
addr = (ip,port)
#tcp协议
ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(addr)
ss.listen(2)
pics = b""
conn,addr = ss.accept()
while True:
    data = conn.recv(1024)
    if not data:
        break
    pics+= data
base_file = os.path.abspath(__file__)
file_dir = os.path.dirname(base_file)
pic_copy_file_path = os.path.join(file_dir,'test2.gif')
with open(pic_copy_file_path,'wb') as f:
    f.write(pics)
ss.close()