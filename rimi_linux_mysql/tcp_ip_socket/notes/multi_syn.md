# 多线程同步

## 1. 问题解决

1. 关于gil的示例问题，为什么使用多线程之后,加了100w次和减了100w次之后,数值不是为0的
2. 使用dis库来查看字节码

    ```
    
    from dis import dis
    def add1():
        global a
        a += 1

    dis(add1)
    
    
    ```
    
    输出
    
    ```
    19           0 LOAD_GLOBAL              0 (a)
	              2 LOAD_CONST               1 (1)
	              4 INPLACE_ADD
	              6 STORE_GLOBAL             0 (a)
	              8 LOAD_CONST               0 (None)
	             10 RETURN_VALUE
    ```
    
    表示给a加上1这个值
    
3. 为什么我们加上100w 减去100w会出现数字不对的问题,因为为什么使用了多线程来计算,但是由于gil的存在,python同时只会有一个线程在运行,这就涉及到了控制权的问题,gil会分配锁给线程,有锁的线程去执行字节码,但是gil的锁分配是有策略的。比如遇到io操作时候回切换锁,就像我们上面的sleep一样,遇到了sleep程序直接向下执行,不会等待。其实就是gil做的操作。还有比如计算xxx次就会切换操作。比如我们的加减100w次就会在加的途中去切换锁。就可能导致加的时候赋值变量没有执行完，就切换到减法去了。然后数字被减掉了。等等问题导致最后结果不是0

4. 问题解决:

    1. 我们可以使用锁来解决上面的问题
    2. 把a+1的操作锁住,让他不能释放,所以减法就不能去竞争加法时候的锁

    ```
    
    import threading
	from dis import dis
	
	a = 0
	lock = threading.Lock()
	
	
	def add():
	    global a
	    global lock
	    for i in range(100000):
	        lock.acquire()
	        a += 1
	        lock.release()
	
	
	def minus():
	    global a
	    global lock
	    for i in range(100000):
	        lock.acquire()
	        a -= 1
	        lock.release()
	
	
	if __name__ == '__main__':
	    t1 = threading.Thread(target=add)
	    t2 = threading.Thread(target=minus)
	    t1.start()
	    t2.start()
	    t1.join()
	    t2.join()
	    print(a)

    ```
    
  
## 2. 锁的基础



1. 锁有两种状态:锁定和未锁定。而且它也只支持两个函数:获得锁和释放锁
2. 当多线程争夺锁时，允许第一个获得锁的线程进入临界区，并执行代码。所有之后到达 的线程将被阻塞，直到第一个线程执行结束，退出临界区，并释放锁。此时，其他等待的线 程可以获得锁并进入临界区。不过请记住，那些被阻塞的线程是没有顺序的(即不是先到先 执行)，胜出线程的选择是不确定的，而且还会根据 Python 实现的不同而有所区别。

3. 所以说我们就可以在上面的示例代码中加入锁```lock = Lock() ```,然后使用 ``` lock.acquire() ```和 ```  lock.release ```来释放锁
4. 所以我们会说,如果加锁会消耗资源,因为加锁或者释放锁的过程中都会消耗资源

 
## 死锁

1. 我们看这一个例子

    ```
    
    lock = threading.Lock()
	def minus():
	    global a
	    global lock
	    for i in range(100000):
	        lock.acquire()
	        a -= 1
	        lock.acquire()
	        lock.release()
	        lock.release()
	
	
	if __name__ == '__main__':
	    t2 = threading.Thread(target=minus)
	    t2.start()
	    t2.join()
	    print(a)
    
    ```
    
2. 上面的例子程序永远不会结束,因为我们人为的造成了死锁,这是一种死锁产生方式,当线程获取到锁的时候,锁还没有release，就又去申请锁，这个时候,gil由于锁只有释放掉才会准许你去获取锁,所以获取锁的操作一直卡住,程序永远不会结束。

3. RLock 



    1. 上面的问题我们可以使用rlock来解决,一般在程序中我们也会使用rlock来书写程序。因为lock会造成死锁的情况。而rlock很简单。只需要你去申明rlock并且accquire和realse的次数是一样的,那么程序就不会锁住
    2. 代码示例

         ```
         
         lock = threading.RLock()
			def minus():
			    global a
			    global lock
			    for i in range(100000):
			        lock.acquire()
			        a -= 1
			        lock.acquire()
			        lock.release()
			        lock.release()
			
			
			if __name__ == '__main__':
			    t2 = threading.Thread(target=minus)
			    t2.start()
			    t2.join()
			    print(a)
         ```


 

