import socket
IP = '10.2.0.102'
PORT = 19522
address = (IP,PORT)
cli = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cli.connect(address)
# hello 是unicode32的字符集
# 变成utf8进行传输
#python3 使用的是unicode32
while 1:
    input_msg = input('type:')
    cli.send(input_msg.encode('utf-8'))
    #recv会阻塞你的代码
    msg = cli.recv(1024)
    msg = msg.decode('utf8')
    print(msg)
    if msg == 'close connection':
        cli.close()
        break
