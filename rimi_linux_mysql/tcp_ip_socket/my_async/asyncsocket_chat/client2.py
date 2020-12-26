import socket
ss_address = ("0.0.0.0",19528)
ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.connect(ss_address)

while True:
    # data = input('请输入消息:')
    # if not data:
    #     break
    try:
        # ss.send(data.encode('utf8'))
        msg = ss.recv(1024).decode('utf8')
        if not msg:
            print('连接已经关闭')
            ss.close()
            break
        print(msg)
    except Exception:
        print('连接已经关闭')
        break


ss.close()

