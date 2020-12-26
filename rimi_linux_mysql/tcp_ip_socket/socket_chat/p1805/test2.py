# GIL

# python 解释器同一个时间内只能在一个cpu上面运行
from threading import Thread, Lock, RLock
from dis import dis

res = 0
# lock = Lock()
lock = RLock()


# def f1():
#     global res
#     res += 1
#
# print(dis(f1))

# 编译器执行
# 解释器 GIL
# 在执行遇到阻塞的时候,会把你踢出去
# 在执行了xxx行字节码之后,会把你踢出去

def f1():
    global res
    global lock
    # 100亿次 4秒
    for i in range(1000000):
        # 锁住了之后 其他线程就不能来抢占
        lock.acquire()
        lock.acquire()
        res += 1
        lock.release()
        lock.release()


def f2():
    global lock
    global res
    for i in range(1000000):
        lock.acquire()
        res -= 1
        lock.release()


t1 = Thread(target=f1)
t2 = Thread(target=f2)
t1.start()
t2.start()
t1.join()
t2.join()
print(res)
# 死锁
# 对于资源的竞争冲突了
print('over')
