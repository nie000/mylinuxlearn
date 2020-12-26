import threading
from dis import dis

a = 0



def add():
    global a
    global lock
    for i in range(100000):
        lock.acquire()
        a += 1
        lock.release()

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
