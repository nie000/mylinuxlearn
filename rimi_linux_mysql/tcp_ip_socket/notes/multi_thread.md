# 多线程

## 线程和进程

1. 进程

	计算机程序只是存储在磁盘上的可执行二进制(或其他类型)文件。只有把它们加载到 内存中并被操作系统调用，才拥有其生命期。进程(有时称为重量级进程)则是一个执行中 的程序。每个进程都拥有自己的地址空间、内存、数据栈以及其他用于跟踪执行的辅助数据。 操作系统管理其上所有进程的执行，并为这些进程合理地分配时间。进程也可以通过派生
(fork 或 spawn)新的进程来执行其他任务，不过因为每个新进程也都拥有自己的内存和数据 栈等，所以只能采用进程间通信(IPC)的方式共享信息。

2. 线程

    线程(有时候称为轻量级进程)与进程类似，不过它们是在同一个进程下执行的，并 共享相同的上下文。可以将它们认为是在一个主进程或“主线程”中并行运行的一些“迷 你进程”。
线程包括开始、执行顺序和结束三部分。它有一个指令指针，用于记录当前运行的上下 文。当其他线程运行时，它可以被抢占(中断)和临时挂起(也称为睡眠)——这种做法叫 做让步(yielding)。
一个进程中的各个线程与主线程共享同一片数据空间，因此相比于独立的进程而言，线 程间的信息共享和通信更加容易。线程一般是以并发方式执行的，正是由于这种并行和数据 共享机制，使得多任务间的协作成为可能。当然，在单核 CPU 系统中，因为真正的并发是不 可能的，所以线程的执行实际上是这样规划的:每个线程运行一小会儿，然后让步给其他线 程(再次排队等待更多的 CPU 时间)。在整个进程的执行过程中，每个线程执行它自己特定 的任务，在必要时和其他线程进行结果通信。
当然，这种共享并不是没有风险的。如果两个或多个线程访问同一片数据，由于数据访 问顺序不同，可能导致结果不一致。这种情况通常称为竞态条件(race condition)。幸运的是， 大多数线程库都有一些同步原语，以允许线程管理器控制执行和访问。

3. 知乎回答:

	https://www.zhihu.com/question/25532384
	
	这个问题，是操作系统里问的最多的问题之一，也是被误解最深的概念之一。Alan Kay说过，好的角度可以提升80分的智商。理解它们的差别，我从资源使用的角度出发。所谓的资源就是计算机里的中央处理器，内存，文件，网络等等。进程，在一定的环境下，把静态的程序代码运行起来，通过使用不同的资源，来完成一定的任务。比如说，进程的环境包括环境变量，进程所掌控的资源，有中央处理器，有内存，打开的文件，映射的网络端口等等。这里我把进程对内存的管理稍微展开说一下。一个系统中，有很多进程，它们都会使用内存。为了确保内存不被别人使用，每个进程所能访问的内存都是圈好的。一人一份，谁也不干扰谁。还有内存的分页，虚拟地址我就不深入探讨了。这里给大家想强调的就是，进程需要管理好它的资源。其中，线程作为进程的一部分，扮演的角色就是怎么利用中央处理器去运行代码。这其中牵扯到的最重要资源的是中央处理器和其中的寄存器，和线程的栈（stack）。这里想强调的是，线程关注的是中央处理器的运行，而不是内存等资源的管理。当只有一个中央处理器的时候，进程中只需要一个线程就够了。随着多处理器的发展，一个进程中可以有多个线程，来并行的完成任务。比如说，一个web服务器，在接受一个新的请求的时候，可以大动干戈的fork一个子进程去处理这个请求，也可以只在进程内部创建一个新的线程来处理。线程更加轻便一点。线程可以有很多，但他们并不会改变进程对内存（heap）等资源的管理，线程之间会共享这些资源。总结一下，我上面的解释是通过计算机操作系统的角度出发的。进程和线程不是同一个层面上的概念，线程是进程的一部分，线程主抓中央处理器执行代码的过程，其余的资源的保护和管理由整个进程去完成。`

## GIL

1. 说明:
    Python 代码的执行是由 Python 虚拟机(又名解释器主循环)进行控制的。Python 在 设计时是这样考虑的，在主循环中同时只能有一个控制线程在执行，就像单核 CPU 系统 中的多进程一样。内存中可以有许多程序，但是在任意给定时刻只能有一个程序在运行。 同理，尽管 Python 解释器中可以运行多个线程，但是在任意给定时刻只有一个线程会被 解释器执行。
    
2. 执行方式:

    在多线程环境中，Python 虚拟机将按照下面所述的方式执行。
    
	1. 设置 GIL。
	2. 切换进一个线程去运行。 
	3. 执行下面操作之一。
	
	    a.指定数量的字节码指令。
	    
	    b.线程主动让出控制权(可以调用 time.sleep(0)来完成)。 4.把线程设置回睡眠状态(切换出线程)。
	5. 解锁 GIL。
	6. 重复上述步骤。

3. 线程简单的使用

	1. 没有使用线程的程序,每个函数会从上向下执行

		> tcp_ip_socket/multi/v1_basic/no_thread.py
		
		```
		import time

		def lo1():
		    time.sleep(4)
		    print('<------lo1-------->')
		
		
		def lo2():
		    time.sleep(2)
		    print('<------lo1-------->')
		
		
		def main():
		    t1 = time.time()
		    lo1()
		    lo2()
		    t2 = time.time()
		
		    print('total time: {}'.format(t2-t1))
		
		if __name__ == "__main__":
		    main()
		```
		
	2. 使用多线程来优化程序
	    在执行lo1的时候,因为要睡眠4秒,但是没有必要去等待lo1,lo2可以使用另外一个线程去执行lo2

		> tcp_ip_socket/multi/v1_basic/thread.py
		
	    ```
	    
	    import time
		import threading
		
		def lo1():
		    time.sleep(4)
		    print('<------lo1-------->')
		
		
		def lo2():
		    time.sleep(2)
		    print('<------lo1-------->')
		
		
		def main():
		    t1 = time.time()
		    f1 = threading.Thread(target=lo1)
		    f2 = threading.Thread(target=lo2)
		    f1.start()
		    f2.start()
		    f1.join()
		    f2.join()
		    t2 = time.time()
		
		    print('total time: {}'.format(t2-t1))
		
		if __name__ == "__main__":
		    main()
	    
	    ```

4. gil的问题

	我们使用多线程去给一个数加100w次,再减100w次最后看这个数是多少
	
	```
	import threading
	a = 0
	def add():
	    global a
	    for i in range(1000000):
	        a += 1
	def minus():
	    global a
	    for i  in range(1000000):
	        a -= 1
	def main():
	threading.Thread(target=add).start()
	threading.Thread(target=minus).start()
	if __name__ == '__main__':
	    main()
	    print(a)
	```
	
	我们会在后面的锁来解释这个问题
	
## 线程的基本使用方式

1. threading模块

    1. 使用threading的Thread模块来申明函数使用多线程来执行

       1. 使用threading的Thread库来初始化线程
       2. 使用target来指明函数,不要加括号
       3. 参数的传递写在 args里面 以tuple的形式
       4. 但是这个函数有一个问题,他不会执行,因为main函数有一个隐藏的主线程,所以虽然我们new出来了两个新线程,但是主线程立刻执行,然后两个线程才会执行。因为要睡眠后才打印
		
		> tcp_ip_socket/multi/v2_basic_usage/v2_basic_usage.py
		
	    ```
		import threading
		import time
		
		def lo1(a):
		    time.sleep(4)
		    print(a)
		
		
		def lo2(b):
		    time.sleep(2)
		    print(b)
		
		
		def start():
		    threading.Thread(target=lo1,args=(2,)).start()
		    threading.Thread(target=lo2, args=(3,)).start()
		
		    print(4)
		
		
		if __name__ == '__main__':
		    start()
	    ```
    
    2. 使用join函数阻塞主线程

    	1. 解决上面的问题的方式是可以在主线程调用两个子线程之后,阻塞4秒 等待两个子线程完成后打印主线程的东西

    	```
    	import threading
		import time
		
		def lo1(a):
		    time.sleep(4)
		    print(a)
		
		
		def lo2(b):
		    time.sleep(2)
		    print(b)
		
		
		def start():
		    t1= threading.Thread(target=lo1,args=(2,))
		    t2= threading.Thread(target=lo2, args=(3,))
		
		    t1.start()
		    t2.start()
		
		    time.sleep(6)
		
		    print(4)
		
		
		if __name__ == '__main__':
		    start()
    	```
    	
    2. 但是在正常情况下我们是不会去估算程序的时间的,需要程序自己去阻塞

    	1. 说明:所以我们可以使用线程自带的join方法,join方式的使用方式是现在阻塞在那里,等待所有调用join方式的线程执行完毕之后才会向下去执行

	    ```
	    import threading
		import time
		def lo1(a):
		    time.sleep(4)
		    print(a)
		def lo2(b):
		    time.sleep(2)
		    print(b)
		def start():
		    t1 = threading.Thread(target=lo1, args=(2,))
		    t2 = threading.Thread(target=lo2, args=(3,))
		    t1.start()
		    t2.start()
		    t1.join()
		    t2.join()
		    print(4)
		if __name__ == '__main__':
		    start()
	    ```
	    
	3. 使用类的方式调用多线程

		1. 首先继承threading.Thread类
		2. 在init中直接先申明父类init方法(super()),再接受 target args两个属性.和上面的函数方法一样
		3. 重要的是run方法,线程调用的时候,就会执行run方法
				
		> tcp_ip_socket/multi/v2_basic_usage/v2_class_usage.py
  
	   ```
	
		import threading
		import time
		
		
		class TestThread(threading.Thread):
		    def __init__(self, target=None, args=None):
		        # 调用父类方法
		        super().__init__()
		        self.target = target
		        self.args = args
		
		    # 当调用函数的时候使用的方法
		    def run(self):
		        self.target(*self.args)
		
		
		def test(i):
		    time.sleep(i)
		    print('execute thread:{}'.format(i))
		
		
		def loop():
		    my_tasks = []
		    for i in range(5):
		        my_tasks.append(TestThread(target=test, args=(i,)))
		    for i in my_tasks:
		        i.start()
		    for i in my_tasks:
		        i.join()
		    print("all down")
		
		loop()

	   
	    ```
	    
	    
## 线程的练习

1. 使用socket获取报文的函数来获取伯乐在线的多个文章 http://blog.jobbole.com/114297/ 每个文章都是以编号来区分的,我们随机生成编号来获取多个文章，书写单线程和多线程 查看时间差异

	> 单线程
	
	> v2_practice1.py
	
	```
	
	#封装http请求报文 多线程请求和单线程请求的不同
	from http_req import get_url
	from urllib.parse import urljoin
	from v2_class_usage import TestThread
	import time
	
	
	def loop1():
	    #单线程获取方式
	    # http://blog.jobbole.com/114297/
	    domain = "http://blog.jobbole.com/"
	    for i in range(114297,114320):
	        i = str(i)
	        url = urljoin(domain,i)
	        get_url(url)
	
	
	
	if __name__ == "__main__":
	    t1 = time.time()
	    loop1()
	
	    t2 = time.time()
	
	    print('---------')
	    print(t2-t1)
	
	```
	
	>多线程
	
    >v2_practice1.py
    
    ```
	    #封装http请求报文 多线程请求和单线程请求的不同
	from http_req import get_url
	from urllib.parse import urljoin
	from v2_class_usage import TestThread
	import time
	
	
	def loop1():
	    #单线程获取方式
	    # http://blog.jobbole.com/114297/
	    domain = "http://blog.jobbole.com/"
	    for i in range(114297,114320):
	        i = str(i)
	        url = urljoin(domain,i)
	        t = TestThread(target=get_url,args=(url,))
	        t.start()
	
	
	
	if __name__ == "__main__":
	    t1 = time.time()
	    loop1()
	
	    t2 = time.time()
	
	    print('---------')
	    print(t2-t1)
    ```
    

2. 多线程请求  ```  https://www.jb51.net/article/112719.htm ```



    



	
