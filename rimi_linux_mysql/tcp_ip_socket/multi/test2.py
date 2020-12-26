
import time
import threading
from threading import Lock
import random
import dis
#任务列表
lock = Lock()
i = 5

def plus():

    global j
    for i in range(1000000):
        #获取这个锁才能执行这个代码
        # 获取锁的前提
        # 没有锁
        lock.acquire()
        j +=1
        # 等待解锁
        lock.acquire()
        lock.release()


def minus():

    global j
    for i in range(1000000):
        lock.acquire()
        j -=1
        time.sleep(2)
        lock.release()
        #不让一个线程运算太多
        #让阻塞操作切换出去

def test():
    global j
    j = j -1

#gil 管理线程
if __name__ == '__main__':
    # dis.dis(test)
    # j = 0
    t1 = threading.Thread(target=plus)
    t2 = threading.Thread(target=minus)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
