import socket
import select

# 创建socket对象,绑定IP端口,监听
sk = socket.socket()
sk.bind(('127.0.0.1', 19851))
sk.listen(5)

inputs = [sk]
outputs = []
while True:
    rList, wList, e = select.select(inputs, outputs, [], 1)
    print("---" * 20)
    print("select当前监听inputs对象的数量>", len(inputs), " | 发生变化的socket数量>", len(rList))
    print("select当前监听outputs对象的数量>", len(outputs), " | 需要回复客户端消息的数量>", len(wList))

    # 遍历rList(建立连接和接收数据)
    for s in rList:
        # 判断socket对象如果是服务端的socket对象的话
        if s == sk:
            conn, address = s.accept()
            # conn也是一个socket对象
            # 当服务端socket接收到客户的请求后,会分配一个新的socket对象专门用来和这个客户端进行连接通信

            # 当服务端分配新的socket对象给新连接进来的客户端的时候
            # 我们也需要监听这个客户端的socket对象是否会发生变化
            # 一旦发生变化,意味着客户端向服务器端发来了消息
            inputs.append(conn)
            conn.sendall(bytes('hello', encoding='utf8'))
        # 其他的就都是客户端的socket对象了
        else:
            try:
                # 意味着客户端给服务端发送消息了
                msg = s.recv(1024)

                # Linux平台下的处理
                if not msg:
                    raise Exception('客户端已断开连接')
                else:
                    outputs.append(s)
                    print(msg)

                # 向客户端回复消息
                # 这种写法是完全可以的,但是缺点是读写都混在了一起
                # s.sendall(msg)
            except Exception as ex:
                # Windows平台下的处理
                inputs.remove(s)

    # 遍历wList(遍历给服务端发送过消息的客户端)
    for s in wList:

        # 给所有的客户端统一回复内容
        s.sendall(bytes('server response', encoding='utf8'))

        # 回复完成后,一定要将outputs中该socket对象移除
        outputs.remove(s)
