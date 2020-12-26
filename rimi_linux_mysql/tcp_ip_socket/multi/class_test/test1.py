import time
import threading

def lo1(num):
    time.sleep(4)
    print(num)
    print('<------lo1-------->')


def lo2():
    time.sleep(2)
    print('<------lo2-------->')


def main():
    t1 = time.time()
    thread1 = threading.Thread(target=lo1,args=(1,))
    thread2 = threading.Thread(target=lo2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    #join 阻塞主线程
    t2 = time.time()

    print('total time: {}'.format(t2-t1))

if __name__ == "__main__":
    main()