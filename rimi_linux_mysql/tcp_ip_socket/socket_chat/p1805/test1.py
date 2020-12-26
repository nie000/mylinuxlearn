from threading import Thread
import time


def f1(x, y):
    print(x, y)
    time.sleep(5)
    print('f1')


def f2(z):
    print(z)
    time.sleep(3)
    print('f2')


# t1 t2线程对象
t1 = Thread(target=f1, args=('5', '4'))
t2 = Thread(target=f2, args=('x',))
t1.start()
t2.start()

t1.join()
t2.join()
print('asdf')
# 3个 主线程
