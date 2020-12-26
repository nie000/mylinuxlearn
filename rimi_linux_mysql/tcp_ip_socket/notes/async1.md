# asyncio 原生协程

#### asyncio的作用

1. 包含各种特定系统实现的模块化事件循环
2. 传输和协议抽象
3. 对tcp,upd,ssl,子进程,延时调用以及其他的具体支持
4. 模仿futures模块但适用于事件循环使用的Future类
5. 基于yield from的协议和任务,可以让你用顺序的方式编写并发代码
6. 必须使用一个将产生阻塞io的调动时,有接口可以把这个事件转移到线程池
7. 模仿threading模块中的同步原语,可以在单线程协程内调用

8. 总结: asyncio库是一个python实现了原生协程异步等功能的库,并且可以让我们使用顺序的方式编程,不用考虑事件循环以及事件循环的变量传递问题。他是Python解决异步io编程的一整套解决方案 

#### asyncio的基础使用

使用的方式:
    事件循环+驱动协程+io多路复用
    
1. 基本使用方式
	1. 协程使用async定义
	2. await 后面跟上io操作
	3. async 中不能写入阻塞io操作

	>yield from 用法
	
	```
	
	import asyncio
	import time
	
	@asyncio.coroutine
	def get_html(url):
	    print('start get url',url)
	    yield from asyncio.sleep(2)
	    print('end get url',url)
	
	if __name__ == '__main__':
	    start_time = time.time()
	    loop = asyncio.get_event_loop()
	    loop.run_until_complete(get_html('sadf'))
	
	```

	>原生协程用法
	
	```
	
	import asyncio
	import time
	#协程中是不能使用同步阻塞编程的
	async def get_html(url):
	    print('start get url',url)
	    await asyncio.sleep(2)
	    print('end get url')
	
	if __name__ == '__main__':
	    start_time = time.time()
	    #事件循环,代替自己写的loop
	    loop = asyncio.get_event_loop()
	    loop.run_until_complete(get_html("ww.baidu.com"))
	    print('times',time.time()-start_time)
	```
	
2. 多个任务提交

	1. 把任务完批量提交给asyncio进行完成
	2. 为什么不能用sleep,当loop循环到sleep的时候,如果使用await的时候,就会直接向下执行,不会阻塞,但是如果使用time.sleep的话,那么程序会阻塞,等到sleep完成后再向下执行。

	```
	
	import asyncio
	import time
	
	
	@asyncio.coroutine
	def get_html(times):
	    print('start get url'.format(times))
	    yield from asyncio.sleep(times)
	    print('end get url {}'.format(times))
	
	
	if __name__ == '__main__':
	    start_time = time.time()
	    loop = asyncio.get_event_loop()
	    tasks = list()
	    for i in range(1, 10):
	        tasks.append(get_html(i))
	
	    loop.run_until_complete(asyncio.wait(tasks))
	```

	```	
	import asyncio
	import time
	#协程中是不能使用同步阻塞编程的
	async def get_html(url):
	    print('start get url',url)
	    await asyncio.sleep(2)
	    print('end get url')
	
	if __name__ == '__main__':
	    start_time = time.time()
	    #事件循环,代替自己写的loop
	    loop = asyncio.get_event_loop()
	    tasks = [get_html('www.baidu.com') for i in range(10)]
	    loop.run_until_complete(asyncio.wait(tasks))
	    print('times',time.time()-start_time)
	
	
	```
	
3. 获取async返回值

    1. 使用 ```asyncio.ensure_future(get_html('www.baidu.com'))```futures类来给出结果的期望在循环调用完成后获取返回结果
    2. 使用 ``` loop.create_task(get_html('www.baidu.com'))``` 直接添加到循环中来表示想获取到结果

    3. 使用 ```  add_done_callback(call_back)```可以添加回调函数,通知一个函数表示这个函数已经完成

    ```
    
    import asyncio
	import time
	
	
	# 协程中是不能使用同步阻塞编程的
	async def get_html(url):
	    print('start get url', url)
	    await asyncio.sleep(2)
	    print('end get url')
	    return 'get_futures'
	
	
	# 函数必须要使用到future,就是完成好的函数
	def call_back(future):
	    print('tasks compete')
	
	
	if __name__ == '__main__':
	    start_time = time.time()
	    # 事件循环,代替自己写的loop
	    loop = asyncio.get_event_loop()
	    # 1.使用future,获取future期望,传递给loop
	    # get_future = asyncio.ensure_future(get_html('www.baidu.com'))
	    get_future = loop.create_task(get_html('www.baidu.com'))
	    # 把结果返回给callback函数
	    get_future.add_done_callback(call_back)
	    loop.run_until_complete(get_future)
	    print('times', time.time() - start_time)
	    print(get_future.result())
    
    ```
    
4. wait 和 gather

	1. wait和gather都表示等待任务完成
	2. gather可以接受过个任务组来执行
	
		```
			
		import asyncio
		import time
		#协程中是不能使用同步阻塞编程的
		async def get_html(url):
		    print('start get url',url)
		    await asyncio.sleep(2)
		    print('end get url')
		
		if __name__ == '__main__':
		    start_time = time.time()
		    #事件循环,代替自己写的loop
		    loop = asyncio.get_event_loop()
		    tasks = [get_html('www.baidu.com') for i in range(10)]
		    tasks2 = [get_html('www.google.com') for i in range(10)]
		    # loop.run_until_complete(asyncio.wait(tasks))
		    loop.run_until_complete(asyncio.gather(*tasks,*tasks2))
		    print('times',time.time()-start_time)
	
		
		```
		或者使用
		
		```
		import asyncio
		import time
		#协程中是不能使用同步阻塞编程的
		async def get_html(url):
		    print('start get url',url)
		    await asyncio.sleep(2)
		    print('end get url')
		
		async def get_html2(url):
		    print('start get url',url)
		    await asyncio.sleep(4)
		    print('end get url')
		
		if __name__ == '__main__':
		    start_time = time.time()
		    #事件循环,代替自己写的loop
		    loop = asyncio.get_event_loop()
		    t1 = [get_html('www.baidu.com') for i in range(10)]
		    t2 = [get_html2('www.google.com') for i in range(10)]
		    tasks = asyncio.gather(*t1)
		    tasks2 = asyncio.gather(*t2)
		    # loop.run_until_complete(asyncio.wait(tasks))
		    loop.run_until_complete(asyncio.gather(tasks,tasks2))
		
		    print('times',time.time()-start_time)
	

		```
		
5. 取消协程

	1. 可以使用cancel去取消协程
	
	```
	
	import asyncio
	import time
	#协程中是不能使用同步阻塞编程的
	async def get_html(url):
	    print('start get url',url)
	    await asyncio.sleep(2)
	    print('end get url')
	
	async def get_html2(url):
	    print('start get url',url)
	    await asyncio.sleep(4)
	    print('end get url')
	
	if __name__ == '__main__':
	    start_time = time.time()
	    #事件循环,代替自己写的loop
	    loop = asyncio.get_event_loop()
	    t1 = [get_html('www.baidu.com') for i in range(10)]
	    t2 = [get_html2('www.google.com') for i in range(10)]
	    tasks = asyncio.gather(*t1)
	    tasks2 = asyncio.gather(*t2)
	    # loop.run_until_complete(asyncio.wait(tasks)
	    try:
	        loop.run_until_complete(asyncio.gather(tasks,tasks2))
	    except KeyboardInterrupt:
	        print(tasks2.cancel())
	        loop.close()
	        
	
	
	    print('times',time.time()-start_time)

	```
	
	或者使用
	
	```
	
	import asyncio
	import time
	#协程中是不能使用同步阻塞编程的
	async def get_html(url):
	    print('start get url',url)
	    await asyncio.sleep(2)
	    print('end get url')
	
	async def get_html2(url):
	    print('start get url',url)
	    await asyncio.sleep(4)
	    print('end get url')
	
	if __name__ == '__main__':
	    start_time = time.time()
	    #事件循环,代替自己写的loop
	    loop = asyncio.get_event_loop()
	    t1 = [get_html('www.baidu.com') for i in range(10)]
	    t2 = [get_html2('www.google.com') for i in range(10)]
	    # tasks = asyncio.gather(*t1)
	    # tasks2 = asyncio.gather(*t2)
	    # loop.run_until_complete(asyncio.wait(tasks)
	    try:
	        loop.run_until_complete(asyncio.wait(t1))
	    except KeyboardInterrupt:
	        for task in asyncio.Task.all_tasks():
	            print(task.cancel())
	        loop.stop()
	
	
	
	
	    print('times',time.time()-start_time)
	
	```
	
	
6. stop,close的区别

    1. stop是等待事件循环里面的所有协程执行完成之后停止
    
    2. close 是会清空所有队列和线程池等。

	```
	
	import asyncio
	import time
	def call_back(x):
	    time.sleep(3)
	    print('get',x)
	
	def stoploop(loop):
	    loop.close()
	
	if __name__ == "__main__":
	    loop = asyncio.get_event_loop()
	
	    loop.call_soon(call_back,32)
	    loop.call_soon(stoploop,loop)
	    loop.run_forever()
	
	```

#### call_soon call_later 

1. call_soon和停止循环

	> 解释:
		1. call_soon不会立刻执行,而是等待loop的最新一次循环取执行
		2. 我们可以调用loop.stop()去停止协程的事件循环
		
	
	
	```
	
	import asyncio
	import time
	def call_back(x):
	    time.sleep(3)
	    print('get',x)
	
	def stoploop(loop):
	    loop.stop()
	
	if __name__ == "__main__":
	    loop = asyncio.get_event_loop()
	
	    loop.call_soon(call_back,32)
	    loop.call_soon(stoploop,loop)
	    loop.run_forever()
	
	```
	
2. call_later会让程序延迟（秒）执行

    ```
    
    import asyncio
	import time
	def call_back(x):
	    time.sleep(3)
	    print('get',x)
	
	def stoploop(loop):
	    loop.stop()
	    time.sleep(4)
	    loop.close()
	
	if __name__ == "__main__":
	    loop = asyncio.get_event_loop()
	
	    loop.call_later(3,call_back,32)
	    loop.call_later(2, call_back, 31)
	    # loop.call_later(2,stoploop,loop)
	    loop.run_forever()
    
    ```

3. call_at loop的执行时间戳,loop自己的运行时间戳

    ```
    import asyncio
	import time
	def call_back(x):
	    time.sleep(3)
	    print('get',x)
	
	def stoploop(loop):
	    loop.stop()
	    time.sleep(4)
	    loop.close()
	
	if __name__ == "__main__":
	    loop = asyncio.get_event_loop()
	    now = loop.time()
	    loop.call_at(now+3,call_back,32)
	    loop.call_at(now+2, call_back, 31)
	    loop.run_forever()
    
    ```
    
4. loop.call_soon_threadsafe() 线程安全

	说明: 如果是线程的调用,可以保护线程中的变量的安全
	
	
#### 线程池+asyncio

说明: 使用asyncio的前提是库本身支持,就像http请求,库是没有支持的,如果我们想使用httprequest 那么只好使用多线程,以至于整个主线程不阻塞

	示例代码:
	
	```
	import asyncio
	from concurrent.futures import ThreadPoolExecutor
	import time
	def call_back(x):
	    time.sleep(3)
	    print('get',x)
	
	def stoploop(loop):
	    loop.stop()
	    time.sleep(4)
	    loop.close()
	
	if __name__ == "__main__":
	    loop = asyncio.get_event_loop()
	    ex = ThreadPoolExecutor(max_workers=10)
	    tasks = list()
	    for i in range(20):
	        tasks.append(loop.run_in_executor(ex,call_back,3))
	
	    loop.run_until_complete(asyncio.wait(tasks))
	```
	
#### asyncio http请求(使用tcp)

async自带的有tcp协议,我们不用自己去注册事件,直接使用即可


1. 一次性返回所有结果

	```
	
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
	
	
	
	```
2. 逐个返回结果

    ```
    
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
    
    ```
    


 