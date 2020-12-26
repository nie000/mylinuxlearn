import socket
# 使用tcp连接
import asyncio


async def get_html():
    # 返回读写
    reader, writer = await asyncio.open_connection('www.baidu.com', 80)

    data = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\r\n\r\n".format(
        '/moist-master/rimi_linux_mysql/blob/master/tcp_ip_socket/notes/http_proto.md', 'www.baidu.com').encode('utf8')
    # 发送数据
    writer.write(data)
    print('sended')

    datas = []
    # for 循环不会阻塞
    async for data in reader:
        datas.append(data.decode('utf8'))

    res = "".join(datas)

    return res


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(10):
        tasks.append(asyncio.ensure_future(get_html()))

    loop.run_until_complete(asyncio.wait(tasks))

    for i in tasks:
        print(i.result())

