import threading
from dis import dis

a = 0
lock = threading.RLock()


def add():
    global a
    global lock
    for i in range(100000):
        #gil 加上了之后 gil不会去释放线程
        #gil 执行的是字节码
        # io 的时候把线程踢出去
        # 计算次数过多把线程踢出去
        # 锁为什么不是默认加上的？
        # 锁每次执行都有一个资源的消耗

        #阻塞 等待没有的锁再去加锁
        #永远都不会执行
        lock.acquire()
        lock.acquire()
        # 加锁 释放 加锁 释放
        a += 1
        lock.release()
        lock.release()
        # Rlock 加几次lock 释放几次lock就行了

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
