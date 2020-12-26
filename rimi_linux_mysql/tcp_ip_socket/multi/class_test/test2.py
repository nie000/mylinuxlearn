import threading
from threading import Lock
lock = Lock()

a = 0


def add():
    global a
    for i in range(1000000):
        lock.acquire()
        a += 1
        lock.release()


def minus():
    global a
    for i in range(1000000):
        lock.acquire()
        a -= 1
        lock.release()


def main():
    threading.Thread(target=add).start()
    threading.Thread(target=minus).start()


if __name__ == '__main__':
    main()
    print(a)
