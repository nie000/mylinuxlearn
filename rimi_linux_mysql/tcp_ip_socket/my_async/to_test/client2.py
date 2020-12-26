import socket
from concurrent.futures import ThreadPoolExecutor

def main():
    ss_address = ("0.0.0.0",19528)
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.connect(ss_address)
    ex = ThreadPoolExecutor(max_workers=3)
    ex.submit(say,ss)
    ex.submit(recv,ss)

def recv(ss):
    while True:
        print(ss.recv(1024).decode('utf8'))

def say(ss):
    while True:
        data = input('请输入消息:')
        # if not data:
        #     break
        ss.send(data.encode('utf8'))
        # print(ss.recv(1024).decode('utf8'))


if __name__ == '__main__':
    main()


