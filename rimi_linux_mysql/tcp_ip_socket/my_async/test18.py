import asyncio
async def get_html():
    # 返回读写
    reader, writer = await asyncio.open_connection('www.baidu.com', 80)
    #keep-alive
    data = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\r\n\r\n".format(
        '/moist-master/rimi_linux_mysql/blob/master/tcp_ip_socket/notes/http_proto.md', 'www.baidu.com').encode('utf8')
    # 发送数据
    #ss.send(data)
    writer.write(data)
    datas = []
    # for 循环不会阻塞 reader
    # ss.recv(1024)
    # reader里面的数据要全部接受完成了之后才能去for in
    async for data in reader:
        datas.append(data.decode('utf8'))
    res = "".join(datas)
    return res
async def start():
    tasks = []
    for i in range(10):
        tasks.append(asyncio.ensure_future(get_html()))
    for task in asyncio.as_completed(tasks):
        res = await task
        print(res)
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())