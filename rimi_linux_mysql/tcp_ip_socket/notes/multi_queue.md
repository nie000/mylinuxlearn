## 生产者消费者模型

##### 为什么queue方法是线程安全的

Queue模块提供了一个适用于多线程编程的先进先出数据结构，可以用来安全的传递多线程信息。

它本身就是线程安全的，使用put和get来处理数据，不会产生对一个数据同时读写的问题，所以是安全的。

也就是说在put或者get的时候,就有锁在里面的

部分源码展示

```
class Queue:
    '''Create a queue object with a given maximum size.

    If maxsize is <= 0, the queue size is infinite.
    '''

    def __init__(self, maxsize=0):
        self.maxsize = maxsize
        self._init(maxsize)

        # mutex must be held whenever the queue is mutating.  All methods
        # that acquire mutex must release it before returning.  mutex
        # is shared between the three conditions, so acquiring and
        # releasing the conditions also acquires and releases mutex.
        self.mutex = threading.Lock()
```


##### 基础queue用法展示

1. 说明:

    最后一个例子演示了生产者-消费者模型这个场景。在这个场景下，商品或服务的生产者 生产商品，然后将其放到类似队列的数据结构中。生产商品的时间是不确定的，同样消费者 消费生产者生产的商品的时间也是不确定的。
    

2. 代码示例:

	1. 一个生产者不断的放入数据
	2. 一个消费者不断的取消费数据
	3. 他们两个是独立运行的,生产者只管像生产线中去放入数据,消费者只管向生产线中去取出数据消费
	4. queue的用法
	    1. 使用queue.Queue()去初始化一个普通的队列,其中可以去设置队列的最大值
	    2. 使用put去向队列中加入数据,当加入的数据满了之后,put方法就会阻塞
	    3. 使用get方法去获取队列中的值,如果队列中没有值,那么get方法就会阻塞

		```
			
			# 两个队列,一个生产者不断的去队列里面存放任务,一个消费者,不断的取队列里面消费任务
		import time
		import random
		import queue
		import threading
		
		
		def product_task_to_queue(queue):
		    '''
		    不断的像队列中去加入任务,每隔1，3秒加入一次
		    :return:
		    '''
		    task_num = 1
		    while True:
		        print('product task', str(task_num),'task_size',queue.qsize())
		        queue.put(str(task_num))
		        sleep_time = random.randint(1, 2)
		        time.sleep(sleep_time)
		        task_num += 1
		
		
		def consume_task_from_queue(queue):
		    """
		    不断的向队列中获取任务,然后消费任务,每隔2-4秒消费一次
		    :param queue:
		    :return:
		    """
		    while True:
		        task_num = queue.get()
		        sleep_time = random.randint(3, 4)
		        time.sleep(sleep_time)
		        consume_task(task_num,queue)
		
		
		def consume_task(task_num,queue):
		    """
		    消费任务的函数
		    :param task_num:
		    :return:
		    """
		    print('consume task num:', task_num,'task_size',queue.qsize())
		
		
		def loop():
		    que = queue.Queue(maxsize=10)
		    t1 = threading.Thread(target=product_task_to_queue,args=(que,))
		    t2 = threading.Thread(target=consume_task_from_queue, args=(que,))
		
		
		    t1.start()
		    t2.start()
		    t1.join()
		    t2.join()
		
		loop()
		
		```
		
##### 爬虫用法

1. 一个程序不断的向队列中去写入数据
2. 另一个程序不断的向队列中去读取数据

	```
	import requests
	from bs4 import BeautifulSoup
	from queue import Queue
	from threading import Thread
	
	
	def get_html_doc(url):
	    # 根据指定的url获取html文档
	    res = requests.get(url)
	    print(res.content)
	    return res.content.decode("utf8")


	def get_detail(que):
	    while True:
	        url = que.get()
	        Thread(target=get_html_doc, args=(url,))
	
	
	def parse_index(url, que, index_urls_list):
	    # 解析列表页面
	    html_doc = get_html_doc(url)
	    data = BeautifulSoup(html_doc)
	    # 把index里面的url取出来再取下面的url
	    # data.select调用css选择器 选择出来是dict
	    detail_urls = data.select('[class=post-thumb] a')
	    # 获取细节的url,把细节的url交给其他线程处理
	    for i in detail_urls:
	        que.append(i)
	    # 取出所有其他index页面的翻页url 去解析其他的url
	    index_urls = data.select('a[class=page-numbers]')
	    for i in index_urls:
	        # 保证不重复
	        if i not in index_urls_list:
	            index_urls_list.append(i)
	            url = i['href']
	            Thread(target=parse_index, args=(url, que))
	
	
	def start(url, que, index_urls_list):
	    parse_index(url, que, index_urls_list)
	
	
	if __name__ == "__main__":
	    url = "http://blog.jobbole.com/category/it-tech/"
	    que = Queue()
	    index_urls_list = Queue()
	
	    start(url, que, index_urls_list)
	
	```
	
3. queue的方式进行同步:

	1. threading自带的queue结构可以在线程中去共享变量,并且queue的数据结构中有锁机制,不会引发多线程的gil字节码的问题
	2. 我们去优化之前的爬虫代码,使他有多线程的机制,我们先做一个简单的队列,只取一个列表页,然后向queue中写入url,然后另一个专门获取详情页的线程去获取详情页面

	```
	
	import requests
	from bs4 import BeautifulSoup
	from queue import Queue
	from threading import Thread
	import time
	
	
	def get_html_doc(url):
	    # 根据指定的url获取html文档
	    res = requests.get(url)
	    print(res.content)
	    return res.content.decode("utf8")
	
	
	def get_detail(detail_urls_queue):
	    while True:
	        url = detail_urls_queue.get(1,timeout=2)
	        print('consumer--->',url)
	        get_html_doc(url)
	
	
	def parse_index(url, detail_urls_queue):
	    # 解析列表页面
	    html_doc = get_html_doc(url)
	    data = BeautifulSoup(html_doc)

    # 把index里面的url取出来再取下面的url
    # data.select调用css选择器 选择出来是dict
    detail_urls = data.select('[class=post-thumb] a')
    # 获取细节的url,把细节的url交给其他线程处理
    for i in detail_urls:
        url = i['href']
        print('productor------>',url)
        detail_urls_queue.put(url)
       
		if __name__ == "__main__":
		    url = "http://blog.jobbole.com/category/it-tech/"
		    # 详细页面的url
		    detail_urls = Queue(100)
		    # 列表url 防止重复
		    # index_urls_list = []
		    t1 = Thread(target=parse_index,args=(url,detail_urls))
		    t2 = Thread(target=get_detail, args=(detail_urls,))
		    t1.start()
		    t2.start()
		    # parse_index(url, detail_urls, index_urls_list)
		    t1.join()
		    t2.join()
		    print('down')

	
	```
	
4. 完善的多线程获取页面方式

	1. 说明:
		1. 把列表页的url加入
		2. 列表页也不断的去循环列表页的url

	```
		
	import requests
	from bs4 import BeautifulSoup
	from queue import Queue
	from threading import Thread,RLock
	
	
	def get_html_doc(url):
	    # 根据指定的url获取html文档
	    res = requests.get(url)
	    # print(res.content)
	    return res.content.decode("utf8")
	
	
	def get_detail(detail_urls_queue):
	    while True:
	        url = detail_urls_queue.get(1, timeout=2)
	        print('consumer--->', url)
	        get_html_doc(url)
	
	
	def parse_index(detail_urls_queue, index_urls_queue,index_urls_queue_record):
	    while True:
	        url = index_urls_queue.get(1)
	        print('get_index_url--->', url)
	        # 解析列表页面
	        html_doc = get_html_doc(url)
	        data = BeautifulSoup(html_doc)
	
	        # 把index里面的url取出来再取下面的url
	        # data.select调用css选择器 选择出来是dict
	        detail_urls = data.select('[class=post-thumb] a')
	        # 获取细节的url,把细节的url交给其他线程处理
	        for i in detail_urls:
	            url = i['href']
	            print('productor------>', url)
	            detail_urls_queue.put(url)
	
	        # 取出所有其他index页面的翻页url 去解析其他的url
	        index_urls = data.select('a[class=page-numbers]')
	        for i in index_urls:
	            if i in index_urls_queue_record:
	                continue
	            url = i['href']
	            index_urls_queue.put(url)
	            #在添加的时候,不要让gil去释放锁
	            locks.acquire()
	            index_urls_queue_record.append(url)
	            locks.release()
	            print('put_index_url--->', url)
	            # 去重 使用redis数据库
	
	
	if __name__ == "__main__":
	    url = "http://blog.jobbole.com/category/it-tech/"
	    # 详细页面的url
       detail_urls = Queue(40)
       index_urls_queue = Queue(5)
	    index_urls_queue.put(url)
	    #记录重复url
	    index_urls_queue_record = [url]
	    locks = RLock()
	    # 列表url 防止重复
	    # index_urls_list = []
	    t1 = Thread(target=parse_index, args=(detail_urls, index_urls_queue,index_urls_queue_record,locks))
	    t2 = Thread(target=get_detail, args=(detail_urls,))
	    t1.start()
	    t2.start()
	    t1.join()
	    t2.join()
	    print('down')


	
	```

## 线程池


##### 简单的示例

给出一个任务,然后交给线程池完成,线程池可以设置最大线程的数量,所以他会一次执行三个

```

from concurrent.futures import ThreadPoolExecutor
import time

#简单的线程池使用
def consume(num):
    time.sleep(2)
    print('consuming',num)

pools = ThreadPoolExecutor(3)

num = 1
while True:

    time.sleep(0.5)
    pools.submit(consume,(num))
    num += 1


```

1. 说明:
	1. 什么是线程池,顾名思义就是首先把多个线程放入一个池子中（内存）,当有剩余的线程的时候,我们就把线程取出来使用,如果没有剩余的线程,程序就会等待线程
	2. 使用线程池我们可以获取到任务的返回结果
	
2. 基本使用方式:

	1. 继承 ``` concurrent.futures  ```库来实现多线程库
	2. max_workers表示线程池中最大有多少个线程
	3. submit表示把任务提交给线程池
	4. done方法可以查看任务是否完成(bool)
	5. result 方式会阻塞程序,等待线程完成，并且获取函数的返回结果
	6. cancel方式能够取消线程,但是只能取消没有提交上去的线程

    ```
    
	from concurrent.futures import ThreadPoolExecutor
	import time
	# 1.并发
	# 2.获取线程的返回值 当一个线程完成的时候,主线程能够知道
	# 3.让多线程和多进程编程接口一致
	def get_html(sleep_time):
	    time.sleep(sleep_time)
	    print("get page {} success".format(sleep_time))
	    return sleep_time
	
	
	executor = ThreadPoolExecutor(max_workers=2)
	#通过sumbit提交到线程池中
	task1 = executor.submit(get_html,(3))
	task2 = executor.submit(get_html,(2))
	task3 = executor.submit(get_html,(2))
	
	print(task3.cancel())
	# done 用于判断是否完成
	# print(task1.done())
	# 阻塞 等待任务完成获取结果
	print(task1.result())
	print(task2.result())

    
    ```

3. as_completed 方法
	
	使用 as_completed方法来获取所有完成的线程,并获取返回值
	
	```
	
	from concurrent.futures import ThreadPoolExecutor, as_completed
	import time
	import random
	from functools import partial
	
	def get_html(sleep_time,num):
	    time.sleep(sleep_time)
	    # print("get page {} success".format(sleep_time))
	    return num
	
	
	executor = ThreadPoolExecutor(max_workers=2)
	# 通过sumbit提交到线程池中
	tasks = list()
	for i in range(10):
	    sleep_time = random.randint(2, 5)
	    #把右边函数看成一个整体
	    tasks.append(executor.submit(partial(get_html,sleep_time), (i)))
	#阻塞 等待完成的函数
	for i in as_completed(tasks):
	    data = i.result()
	
	    print('num {} success'.format(data))
		
	```
	
4. wait 阻塞主线程

	wait可以等待tasks的某个任务或者所有任务完成之后再执行其他的(阻塞),
	他有三种可选方式,默认是等待所有tasks完成
	
	1. 等待所有完成
	2. 等待第一个完成
	3. 等待第一个错误
	
	
	```
	
			FIRST_COMPLETED = 'FIRST_COMPLETED'
	FIRST_EXCEPTION = 'FIRST_EXCEPTION'
	ALL_COMPLETED = 'ALL_COMPLETED'
	
	
	from concurrent.futures import ThreadPoolExecutor, as_completed, wait
	import time
	import random
	
	
	def get_html(sleep_time):
	    time.sleep(sleep_time)
	    # print("get page {} success".format(sleep_time))
	    return sleep_time
	
	
	executor = ThreadPoolExecutor(max_workers=2)
	# 通过sumbit提交到线程池中
	tasks = list()
	for i in range(10):
	    sleep_time = random.randint(2, 5)
	    tasks.append(executor.submit(get_html, (sleep_time)))
	
	#阻塞等待任务完成
	wait(tasks, return_when='FIRST_COMPLETED')
	
	for i in as_completed(tasks):
	    data = i.result()
	
	    print('num {} success'.format(data))
	
	print('12312312')	
	
	```
	
5. 示例:

	通过上面的线程池,我们就可以把获取详细页面的任务交给线程池去获取
	
	```
	
	import requests
	from bs4 import BeautifulSoup
	from queue import Queue
	from threading import Thread
	from concurrent.futures import ThreadPoolExecutor
	
	
	def get_html_doc(url):
	    # 根据指定的url获取html文档
	    res = requests.get(url)
	    print('ex--->url',url)
	    return res.content.decode("utf8")
	
	
	def get_detail(detail_urls_queue,pools):
	    while True:
	        url = detail_urls_queue.get(1,timeout=2)
	        # print('consumer--->',url)
	        pools.submit(get_html_doc,(url))
	
	
	def parse_index(detail_urls_queue,index_urls_queue):
	    while True:
	        url = index_urls_queue.get(1)
	        # print('get_index_url--->',url)
	        # 解析列表页面
	        html_doc = get_html_doc(url)
	        data = BeautifulSoup(html_doc)
	
	        # 把index里面的url取出来再取下面的url
	        # data.select调用css选择器 选择出来是dict
	        detail_urls = data.select('[class=post-thumb] a')
	        # 获取细节的url,把细节的url交给其他线程处理
	        for i in detail_urls:
	            url = i['href']
	            # print('productor------>',url)
	            detail_urls_queue.put(url)
	
	
	
	        # 取出所有其他index页面的翻页url 去解析其他的url
	        index_urls = data.select('a[class=page-numbers]')
	        for i in index_urls:
	            url = i['href']
	            index_urls_queue.put(url)
	            #去重 使用redis数据库
	            # print('put_index_url--->', url)
	
	
	if __name__ == "__main__":
	    url = "http://blog.jobbole.com/category/it-tech/"
	    # 详细页面的url
	    detail_urls = Queue()
	    index_urls_queue = Queue()
	    index_urls_queue.put(url)
	    # 列表url 防止重复
	    # index_urls_list = []
	    executor = ThreadPoolExecutor(max_workers=10)
	    t1 = Thread(target=parse_index,args=(detail_urls,index_urls_queue))
	    t2 = Thread(target=get_detail, args=(detail_urls,executor))
	    t1.start()
	    t2.start()
	    t1.join()
	    t2.join()
	    print('down')
	
	
	```
	
		