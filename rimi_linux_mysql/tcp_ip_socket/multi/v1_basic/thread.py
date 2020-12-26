import time
import threading

def lo1():
    time.sleep(4)
    print('<------lo1-------->')


def lo2():
    time.sleep(2)
    print('<------lo1-------->')


def main():
    t1 = time.time()
    f1 = threading.Thread(target=lo1)
    f2 = threading.Thread(target=lo2)
    f1.start()
    f2.start()
    f1.join()
    f2.join()
    t2 = time.time()

    print('total time: {}'.format(t2-t1))

if __name__ == "__main__":
    main()