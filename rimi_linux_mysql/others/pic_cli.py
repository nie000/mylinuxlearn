# 1. 读取文件（图片）
# 2. 传递读取之后的信息
import os
import socket
pics = b''
base_file = os.path.abspath(__file__)
file_dir = os.path.dirname(base_file)
pic_file_path = os.path.join(file_dir,'test1.gif')
ip = '127.0.0.1'
port = 19527
addr = (ip, port)
#tcp协议
ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.connect(addr)
#python 调用系统底层
with open(pic_file_path,'rb+') as f:
    while True:
        data = f.read(1024)
        if not data:
            break
        pics += data

ss.send(pics)
ss.close()
