# 从生成器到协程

#### 协程的概念

1. 协程不是进程或线程，其执行过程更类似于子例程，或者说不带返回值的函数调用。
2. 一个程序可以包含多个协程，可以对比与一个进程包含多个线程，因而下面我们来比较协程和线程。我们知道多个线程相对独立，有自己的上下文，切换受系统控制；而协程也相对独立，有自己的上下文，但是其切换由自己控制，由当前协程切换到其他协程由当前协程来控制。
3. 从上述字面上的理解为,多线程的暂停与启动是操作系统来控制的,比如gil等。协程是单线程,在单个线程里面能够有能暂停,启动和向函数中去传递值的功能我们就叫做协程。
4. python中 生成器 yield正好有这个暂停和启动的功能。我们可以思考使用生成器来作为协程使用。

#### 生成器的基本行为

1. 控制生成器

	```
	
	def simple_gen1():
	    print('started')
	    x = yield 'running'
	    print('ending',x)
	
	test1 = simple_gen1()
	
	print(next(test1))
	test1.send(1)
	
	```
	
	>输出
	
	```
	
	started
	running
	ending 1
	Traceback (most recent call last):
	File "/Users/canvas/Desktop/project/linux_socket_notes/tcp_ip_socket/yield_from/example_codes/test1.py", line 9, in <module>
	    test1.send(1)
	StopIteration
	
	```
2. 代码解释

    1. yield的右边表示生成一个值,但其实yield左边可以表示接受调用方传递的值,只不过我们一般不会书写,所以它会默认的传递None
    2. 调用next方法去启动生成器。启动之后生成器会在第一个yield的暂停住,并且生成出一个值,值是 yield表达式右边的值。
    3. 调用send方法,yield左边会接受值,并且向下执行,如果没有yield暂停则会抛出stopItertion的异常出来

    4. 通过上面的代码我们看出,生成器可以暂停，和接受值。他有协程的特征存在。

3. 查看生成器的状态

    ```
    
    from inspect import getgeneratorstate
	def simple_gen1():
	    print('started')
	    x = yield 'running'
	    print('receive_x:',x)
	    y = yield x
	    print('receive_y:', y)
	
	
	test1 = simple_gen1()
	
	print(getgeneratorstate(test1))
	
	next(test1)
	print(getgeneratorstate(test1))
	next(test1)
	print(getgeneratorstate(test1))
	try:
	    next(test1)
	except Exception:
	    pass
	print(getgeneratorstate(test1))
    
    ```
    输出
    
    ```
    
    GEN_CREATED
	started
	GEN_SUSPENDED
	receive_x: None
	GEN_SUSPENDED
	receive_y: None
	GEN_CLOSED
	    
    ```
    
 	>通过上面的代码,我们可以看到 生成器是有状态的--->
 	未激活,暂停中,已经结束
 	
4. 练习题:

	>如下代码会输出多少,并解释运行的过程
	
    ```
    
    def coro(a):
    print('res:',str(a))
    b = yield a
    print('res', str(a+b))
    c = yield b
    print('res', str(a + c))
	
	test1 = coro(5)
	
	next(test1)
	test1.send(6)
	test1.send(9)
    
    ``` 
    
    
5. 我们可以认为,使用yield这种关键字是使用了python的协程,yield既可以作为生成器生成值的关键字,也可以作为python里面的协程使用

6. 协程的用法:

    1. next或者send(none)去激活协程,使他移动到yield处停止
    2. 使用 send 给协程发送值过去,协程向下执行
    3. 使用next就不会发送值,或者发送的值是none。协程向下执行
    4. 使用close可以主动的停止协程
    
#### 生成器练习

1. 一个无限的平均值计算器

    ```
    
    def sum():
    avg = None
    total = 0.0
    num = 0

    while True:
        r = yield avg
        total += r
        num += 1
        avg = total/num



	test = sum()
	next(test)
	print(test.send(1))
	print(test.send(5))
	print(test.send(9))
	print(test.send(89))
    
    ```
    
    > 协程会不断的接受值,然后再yield处生成计算结果,并且暂停等待新的send值过来再循环
    
#### 异常处理

1. 协程内部发生异常之后,会向上冒泡,正如我们之前所看到的,并且会终止协程。终止之后的协程无法重新激活
2. 我们可以使用 throw向协程内部发送异常,并且协程可以catch住异常。

    ```
    
    class DemoException(Exception):
    pass

	def test1():
	    print('start')
	
	    while True:
	        try:
	            x = yield
	        except DemoException:
	            print('demo ex')
	        else:
	            print('receive:',x)
	
	t = test1()
	
	next(t)
	t.send(6)
	t.throw(DemoException)
	t.send(9)
    
    ```
    
    >我们可以看到,协程抓住了异常并且继续正常运行
    
3. close终止协程

    我们可以看到，close方法会给协程发送StopIteration异常,致使协程停止
    
    ```
    
    class DemoException(Exception):
    pass
	
	def test1():
	    print('start')
	
	    while True:
	        try:
	            x = yield
	        except DemoException:
	            print('demo ex')
	        except StopIteration:
	            print('asdf')
	        else:
	            print('receive:',x)
	
	t = test1()
	
	next(t)
	t.send(6)
	t.throw(DemoException)
	t.send(9)
	t.throw(StopIteration)
	t.send(20)
    
    ```
    
#### 返回值


1. 使用return来返回值
2. 但是,普通的终止下,协程只会返回None
3. 返回的值在StopIertion中

    ```
    
    def sum():
    avg = None
    total = 0.0
    num = 0

    while True:
        r = yield avg
        if r is None:
            break
        total += r
        num += 1
        avg = total/num

    return num,avg
	
	s1 = sum()
	
	next(s1)
	s1.send(5)
	s1.send(8)
	s1.send(10)
	
	try:
	    s1.send(None)
	except Exception as e:
	    print(e.value)
	    
    ```
    
#### 课堂作业


1. 改写下面的代码,使代码能够正常运行,没有报错

    ```
    
    import time
	import random
	
	def consume():
	    while True:
	        product = yield
	        print('consume product:',product)
	        if product == 5:
	            return '收到5'
	
	def product():
	    t = consume()
	    while True:
	        time.sleep(random.randint(0,1))
	        t.send(random.randint(1,10))
	
	product() 
    ```



#### 仿真程序

```
import collections
import queue
import random
Event = collections.namedtuple('Event', 'time proc action')


def taxi_process(ident, trips, start_time=0):
    time = yield Event(start_time, ident, 'leave garage')
    for i in range(trips):
        time = yield Event(time, ident, 'pick up passenger')
        time = yield Event(time, ident, 'drop off passenger')

    yield Event(time, ident, 'going home')


class Simulator:

    def __init__(self,taxis):

        self.events = queue.PriorityQueue()
        self.taxis = taxis.copy()

    def run(self,end_time):
        for _,i in self.taxis.items():
            first_event = next(i)
            self.events.put(first_event)

        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():
                print('end events')
                break
            current_event = self.events.get()
            sim_time,taxi_id,actions = current_event
            print('taxi:',taxi_id,'at:',sim_time,'do',current_event)
            next_time = sim_time + random.randint(1,8)
            try:
                next_event = self.taxis[taxi_id].send(next_time)
            except StopIteration:
                del self.taxis[taxi_id]
            else:
                self.events.put(next_event)
        else:
            print('time out')

def main(taxi_num):
    taxis = dict()
    for i in range(taxi_num):
        #生成出租车的对象,间隔发车,运营次数随机
        taxis[i] = taxi_process(i, random.randint(10,20), start_time=random.randint(0,10))
    sim = Simulator(taxis)
    sim.run(120)



if __name__ == '__main__':
    # taxi = taxi_process(ident=5,trips=2,start_time=7)
    # print((next(taxi)))
    # print(taxi.send(9))
    # print(taxi.send(14))
    # print(taxi.send(24))
    # print(taxi.send(34))
    # print(taxi.send(44))
    # print(taxi.send(54))
    # print(taxi.send(64))
    main(9)


```