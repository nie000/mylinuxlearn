# select 函数的使用

## 前置知识点

1. https://www.jianshu.com/p/f11724034d50
2. https://blog.csdn.net/summy_J/article/details/74474902
3. https://www.cnblogs.com/wxl-dede/p/5134636.html
4. https://www.jianshu.com/p/dfd940e7fca2
5. https://blog.csdn.net/lihao21/article/details/67631516?ref=myread
6. https://blog.csdn.net/lixiaoguang20/article/details/53929869

7. select vs epoll 连接数量不高但是很活跃select 连接数量搞但是不活跃 epoll

## select模块的使用

select会监听socket或者文件描述符的I/O状态变化，并返回变化的socket或者文件描述符对象

```
select(rlist, wlist, xlist[, timeout]) -> (rlist, wlist, xlist)
```

这是Python select方法的原型，接收4个参数

1. rlist：list类型，监听其中的socket或者文件描述符是否变为可读状态，返回那些可读的socket或者文件描述符组成的list
2. wlist：list类型，监听其中的socket或者文件描述符是否变为可写状态，返回那些可写的socket或者文件描述符组成的list
3. xlist：list类型，监听其中的socket或者文件描述符是否出错，返回那些出错的socket或者文件描述符组成的list
4. timeout：设置select的超时时间，设置为None代表永远不会超时，即阻塞。

>注意：Python的select方法在Windows和Linux环境下的表现是不一样的，Windows下它只支持socket对象，不支持文件描述符（file descriptions)，而Linux两者都支持。

1. 我们可以通过打印来查看select模块提供的作用

>1. 他返回的rlist,wlist只会返回有<b>改变</b>的监听对象,如果没有改变的函数,那么整个程序会阻塞住
>2. 如果我们想要加入新的连接,那么我们只需要把连接对象放进rlist即可，当有数据过来的时候,那么连接就会发生改变(文件描述符),select函数就会帮我们监听到
>3. 如果我们想发送数据,那么我们可以把conn加入到wlist,因为发送数据需要我们去输出流数据,然后等待select把wlist里面的消息取出来,我们就可以发送数据了

	```
	
	# python select io多路复用测试代码
	# 1. 简单的使用select来进行客户端多连接
	
	import select
	import socket
	import time
	
	# select 把socket放入 select中,然后每当有一个连接过来,把连接conn放入select模型里面去
	
	port = 19834
	ip = "127.0.0.1"
	
	ss = socket.socket()
	ss.bind((ip, port))
	ss.listen(10)
	
	readable_list = [ss]
	
	
	while 1:
	    # print('listen again')
	    rlist, wlist, xlist = select.select(readable_list, [], [],5)
	    # 如果遍历出来的
	    print('listen to the readable sockets',rlist)
	    print('length of the readable sockets',len(rlist))
	    print('length of the total sockets', len(readable_list))
	    for i in rlist:
	        if i is ss:
	            #如果ss准备就绪,那么说明ss就可以接受连接了,当ss接受到连接
	            #那么把连接返回readlist
	            conn,addr = i.accept()
	            readable_list.append(conn)
	
	```
	
2. select 更高级的用法,多用户聊天

	>1. 注意点 每次我们都需要把send的conn给移除出wlist才行,不然每次conn都会准备好写入,无限的循环

	```
	
	# python select io多路复用测试代码
	# 1. 简单的使用select来进行客户端多连接
	
	import select
	import socket
	import time
	
	# select 把socket放入 select中,然后每当有一个连接过来,把连接conn放入select模型里面去
	port = 19860
	ip = "127.0.0.1"
	ss = socket.socket()
	ss.bind((ip, port))
	ss.listen(10)
	read_list = [ss]
	write_list = []
	msg_list = dict()
	while 1:
	    # print('listen again')
	    rlist, wlist, xlist = select.select(read_list, write_list, [], 5)
	    for i in rlist:
	        if i is ss:
	            # 如果ss准备就绪,那么说明ss就可以接受连接了,当ss接受到连接
	            # 那么把连接返回readlist
	            conn, addr = i.accept()
	            read_list.append(conn)
	        # 如果不是socket对象,那么就是conn连接对象了,如果是conn连接对象,那么就代表有
	        # 读入数据的变化,对应recv方法
	        else:
	            try:
	                data = i.recv(1024)
	                # 如果接受不到数据了 则说明连接已经关闭了
	                if not data:
	                    print('connecting close')
	                    read_list.remove(i)
	                    break
	                # 我们去发送数据,但是我们要把conn准备好了再去发送
	                # 所以首先把数据存在一个dict中msg_list,然后再等他准备好的时候
	                # 再去发送
	                msg_list[i] = [data]
	                if i not in write_list:
	                    write_list.append(i)
	            except Exception:
	                read_list.remove(i)
	
	    for j in wlist:
	        # 把对应各自的消息取出来
	        msg = msg_list[j].pop()
	        try:
	            j.send(msg)
	            # 回复完成后,一定要将outputs中该socket对象移除
	            write_list.remove(j)
	        except Exception:
	            # 如果报错就所以连接或者已经断开了,那么我们就把他移出出去
	            write_list.remove(j)

	
	```
	
3. socket群聊,广播聊天消息

	 > server端
	 
    ```
    
    # python select io多路复用测试代码
	# 1. 简单的使用select来进行客户端多连接
	
	import select
	import socket
	import queue
	
	# select 把socket放入 select中,然后每当有一个连接过来,把连接conn放入select模型里面去
	port = 19869
	ip = "127.0.0.1"
	ss = socket.socket()
	ss.bind((ip, port))
	ss.listen(10)
	read_list = [ss]
	write_list = []
	msg_list = []
	while 1:
	    rlist, wlist, xlist = select.select(read_list, write_list, [], 1)
	    for i in rlist:
	        if i is ss:
	            # 如果ss准备就绪,那么说明ss就可以接受连接了,当ss接受到连接
	            # 那么把连接返回readlist
	            conn, addr = i.accept()
	            read_list.append(conn)
	        # 如果不是socket对象,那么就是conn连接对象了,如果是conn连接对象,那么就代表有
	        # 读入数据的变化,对应recv方法
	        else:
	            try:
	                data = i.recv(1024)
	                # 如果接受不到数据了 则说明连接已经关闭了
	                if not data:
	                    print('connecting close')
	                    read_list.remove(i)
	                    break
	                # 我们去发送数据,但是我们要把conn准备好了再去发送
	                # 所以首先把数据存在一个dict中msg_list,然后再等他准备好的时候
	                msg_list.append(data)
	                for i in read_list:
	                    if i is not ss:
	                        write_list.append(i)
	            except Exception:
	                read_list.remove(i)
	    for j in range(len(wlist)):
	        conn = wlist[j]
	        # 把对应各自的消息取出来
	        if j == len(wlist) -1:
	            msg = msg_list.pop()
	        else:
	            msg = msg_list[0]
	        try:
	            conn.send(msg)
	            # 回复完成后,一定要将outputs中该socket对象移除
	            write_list.remove(conn)
	        except Exception:
	            # 如果报错就所以连接或者已经断开了,那么我们就把他移出出去
	            write_list.remove(conn)

    
    ```
    
    > client端（多线程）
    
    ```
    
    # python select io多路复用测试代码
	# 1. 简单的使用select来进行客户端多连接
	
	import select
	import socket
	import threading
	
	# select 把socket放入 select中,然后每当有一个连接过来,把连接conn放入select模型里面去
	
	port = 19869
	ip = "127.0.0.1"
	
	
	def input_line(ss):
	    while True:
	        msg = input("input:")
	        ss.send(msg.encode('utf8'))
	
	def read_line(ss):
	    while True:
	        msg = ss.recv(1024)
	        print('revice from',msg)
	
	def loop():
	    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    ss.connect((ip, port))
	    t1 = threading.Thread(target=input_line,args=(ss,))
	    t2 = threading.Thread(target=read_line, args=(ss,))
	    t1.start()
	    t2.start()
	    t1.join()
	    t2.join()
	
	if __name__ == '__main__':
	    loop()

    
    ```


#### 使用select高效的http请求

```

import select
import socket
from urllib.parse import urlparse


#
class Crawler:
    def __init__(self):
        self.socket_list = []
        self.read_list = list()
        self.write_list = list()
        self.exec_list = list()
        self.req_info = dict()
        self.msg_list = dict()
    #不断的事件循环
    def loop(self):
        while True:
            #
            rlist, wlist, xlist = select.select(self.read_list, self.write_list, self.exec_list)
            for i in wlist:
                # 侦测到写事件 就去发送报文
                host, path = self.req_info[i]
                data = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\r\n\r\n".format(
                    path, host).encode('utf8')
                i.send(data)
                self.write_list.remove(i)
                self.read_list.append(i)
                #侦测到读时间就去获取报文
            for i in rlist:
                msg = i.recv(1024)
                if i not in self.msg_list.keys():
                    self.msg_list[i] = msg
                else:
                    self.msg_list[i] += msg
                    #考虑到网页的大小 一次不可能接受完毕 所以当没有数据的时候才关闭连接
                if not msg:
                    self.read_list.remove(i)
                    print(self.msg_list[i].decode('utf8'))
                    del (self.msg_list[i])

    # 初始化http请求 向类里面不断的添加新的http需求,然后初始化好socket对象 添加给时间循环
    def add_url(self, url):
        # 初始化socket请求
        url_dict = urlparse(url)
        host = url_dict.netloc
        path = url_dict.path
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.connect((host, 80))
        ss.setblocking(False)
        self.write_list.append(ss)
        # 把socket加入socket
        self.socket_list.append(ss)
        self.req_info[ss] = (host, path)


if __name__ == '__main__':
    crawler = Crawler()
    for i in range(100):
        crawler.add_url('https://www.cnblogs.com/myyan/p/7149542.html')
    crawler.loop()

```
## *（自学 了解即可） selector的使用

1. 改造之前的http_req请求的socket函数,不使用select,使用非阻塞io

	1. 我们去设置```ss.setblocking(False)```让他在模型中不去阻塞
	2. 但是我们可以看到connect和recv都在报错,原因是因为系统的io并没有准备好,我们需要去不断的轮询io是否准备好。
	3. 我们可以看到这个方式,并没有提高并发,而且增加了系统的压力

	```
	
	# 使用socket获取http报文
	# 把setblocking设为false 让学员自己解决问题
	import socket
	from urllib.parse import urlparse
	
	# 初始化socket
	domain = "https://book.douban.com/subject/3012360/"
	url = urlparse(domain)
	host = url.netloc
	path = url.path
	if path == "":
	    path = "/"
	ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#使用非阻塞io，socket不等待连接建立好 直接向下执行
	ss.setblocking(False)
	#只有一直try获取连接,因为连接还没有准备好
	while True:
	    try:
	        ss.connect((host, 80))
	    except BlockingIOError as e:
	        pass
	    except OSError:
	        break
	
	#'\r'的本意是回到行首，'\n'的本意是换行
	data = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\r\n\r\n".format(
	    path, host).encode('utf8')
	ss.send(data)
	res = b""
	#报文就不像聊天数据那么小了 需要循环的拼接报文
	#让系统不断遍历 获取到recv因为不是阻塞的
	while True:
	    try:
	        d = ss.recv(1024)
	    except BlockingIOError:
	        continue
	    if d:
	        res += d
	    else:
	        break
	print(res.decode('utf8'))
	ss.close()
	
	
	```
	
2. 使用select 来完成请求

	1. 说明:
	
		1. 使用 ``` from selectors import DefaultSelector ```
		
		2. DefaultSelector可以在linux和windows上面兼容,因为windows没有epoll模型，会切换的select上面去

	2. 代码的修改(http 请求代码)

		1. 我们把所有的非阻塞事件交由select模型去处理
		2. select模型是需要一个主循环去不断的监听描述符,然后等描述符就绪之后,就调用函数

	    ```
	    
	    # 使用socket获取http报文
		# 把setblocking设为false 让学员自己解决问题
		import socket
		from urllib.parse import urlparse
		from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
		
		# 申明select
		sel = DefaultSelector()
		
		
		class Downloader:
		
		    def __init__(self, sel):
		        self.domain = ""
		        self.url = ""
		        self.path = ""
		        self.host = ""
		        self.selector = sel
		        self.ss = ""
		        self.data = b""
		
		    def get_client(self):
		        # 初始化socket
		
		        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		        # 使用非阻塞io，socket不等待连接建立好 直接向下执行
		        self.ss.setblocking(False)
		        # 虽然申明了一个非阻塞操作,但这个还是阻塞操作,不能交给select
		        try:
		            self.ss.connect((self.host, 18001))
		        except Exception:
		            pass
		
		        # 创建好链接之后,向服务器发送http报文,不过这个使用回调的方式来做，这个是一个写操作,因为我们
		        # 向socket中写入数据(发送数据)
		        self.selector.register(self.ss, EVENT_WRITE, self.send_data)
		
		    def send_data(self, mask):
		        # 连接创建好之后去请求http
		        self.selector.unregister(self.ss)
		        data = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\nUser-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\r\n\r\n".format(
		            self.path, self.host).encode('utf8')
		        self.ss.send(data)
		        # 数据发送之后,去获取http数据,这个时候使用读操作
		        self.selector.register(self.ss, EVENT_READ, self.get_http)
		
		    def get_http(self, mask):
		
		        # 在报文没有读取完之前,循环会一直调用这个函数,所以我们不用去
		        # 担心while循环,只需要在他没有报文的时候,结束这个事件就ok了
		        d = self.ss.recv(1024)
		        if d:
		            self.data += d
		        else:
		            self.selector.unregister(self.ss)
		            print(self.data)
		
		    def get_html(self, domain="https://book.douban.com/subject/3012360/"):
		
		        self.domain = domain
		        self.url = urlparse(self.domain)
		        self.host = self.url.netloc
		        self.path = self.url.path
		        if self.path == "":
		            self.path = "/"
		
		        self.get_client()
		
		
		url = 'http://127.0.0.1/index1/'
		# 试着同时获取30条数据
		for i in range(30):
		    download = Downloader(sel)
		    download.get_html(url)
		while True:
		    events = sel.select()
		    for key, mask in events:
		        callback = key.data
		        callback(key)
	    
	    ```
	    
## 水平触发 vs 边缘触发

1. Level_triggered(水平触发)：

	当被监控的文件描述符上有可读写事件发生时，epoll_wait()会通知处理程序去读写。如果这次没有把数据一次性全部读写完(如读写缓冲区太小)，那么下次调用 epoll_wait()时，它还会通知你在上没读写完的文件描述符上继续读写，当然如果你一直不去读写，它会一直通知你！！！如果系统中有大量你不需要读写的就绪文件描述符，而它们每次都会返回，这样会大大降低处理程序检索自己关心的就绪文件描述符的效率！！！

2. Edge_triggered(边缘触发)：

	当被监控的文件描述符上有可读写事件发生时，epoll_wait()会通知处理程序去读写。如果这次没有把数据全部读写完(如读写缓冲区太小)，那么下次调用epoll_wait()时，它不会通知你，也就是它只会通知你一次，直到该文件描述符上出现第二次可读写事件才会通知你！！！这种模式比水平触发效率高，系统不会充斥大量你不关心的就绪文件描述符！！！

3. 几种IO模型的触发方式 

	 select(),poll()模型都是水平触发模式，
	 信号驱动IO是边缘触发模式，
	 epoll()模型即支持水平触发，也支持边缘触发，默认是水平触发。