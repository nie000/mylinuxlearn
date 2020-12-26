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
