# import time
#
# def lo1():
#     time.sleep(4)
#     print('<------lo1-------->')
#
#
# def lo2():
#     time.sleep(2)
#     print('<------lo2-------->')
#
#
# def main():
#     t1 = time.time()
#     lo1()
#     lo2()
#     t2 = time.time()
#
#     print('total time: {}'.format(t2-t1))
#
# if __name__ == "__main__":
#     main()

# import time
# import threading
#
# def lo1():
#     time.sleep(4)
#     print('<------lo1-------->')
#
#
# def lo2():
#     time.sleep(2)
#     print('<------lo2-------->')
#
#
# def main():
#     t1 = time.time()
#     f1 = threading.Thread(target=lo1)
#     f2 = threading.Thread(target=lo2)
#     f1.start()
#     f2.start()
#     print('没有等到')
#     f1.join()
#     f2.join()
#     t2 = time.time()
#
#     print('total time: {}'.format(t2-t1))
#
# if __name__ == "__main__":
#     main()

# import time
# #
# def lo1():
#     a=0
#     for index in range(100000000):
#         a+=index
#     print('<------lo1-------->')
#
#
# def lo2():
#     a = 0
#     for index in range(100000000):
#         a += index
#     print('<------lo2-------->')
#
#
# def main():
#     t1 = time.time()
#     lo1()
#     lo2()
#     t2 = time.time()
#
#     print('total time: {}'.format(t2-t1))
#
# if __name__ == "__main__":
#     main()

# import time
# import threading
#
# def lo1():
#     a=0
#     for index in range(100000000):
#         a+=index
#     print('<------lo1-------->')
#
#
# def lo2():
#     a = 0
#     for index in range(100000000):
#         a += index
#     print('<------lo2-------->')
#
#
# def main():
#     t1 = time.time()
#     f1 = threading.Thread(target=lo1)
#     f2 = threading.Thread(target=lo2)
#     f1.start()
#     f2.start()
#     print('没有等到')
#     f1.join()
#     f2.join()
#     t2 = time.time()
#
#     print('total time: {}'.format(t2-t1))
#
# if __name__ == "__main__":
#     main()


# import time
# import threading
# from multiprocessing import Process
# def lo1():
#     a=0
#     for index in range(100000000):
#         a+=index
#     print('<------lo1-------->')
# def lo2():
#     a = 0
#     for index in range(100000000):
#         a += index
#     print('<------lo2-------->')
# def main():
#     t1 = time.time()
#     f1 =Process(target=lo1)  #进程
#     f2 =Process(target=lo2)  #进程
#     f1.start()
#     f2.start()
#     print('没有等到')
#     f1.join()
#     f2.join()
#     t2 = time.time()
#
#     print('total time: {}'.format(t2-t1))
#
# if __name__ == "__main__":
#     main()


# import time
# import threading
#
# def lo1(a):
#     a=0
#     for index in range(100000000):
#         a+=index
#     print('<------lo1-------->')
#
#
# def lo2(b):
#     a = 0
#     for index in range(100000000):
#         a += index
#     print('<------lo2-------->')
#
#
# def main():
#     t1 = time.time()
#     f1 = threading.Thread(target=lo1,args=(1,))
#     f2 = threading.Thread(target=lo2,args=(2,))
#     f1.start()
#     f2.start()
#     print('没有等到')
#     f1.join()
#     f2.join()
#     t2 = time.time()
#
#     print('total time: {}'.format(t2-t1))
#
# if __name__ == "__main__":
#     main()

# import threading
# import time
#
#
# class TestThread(threading.Thread):
#     def __init__(self, target=None, args=None):
#         # 调用父类方法
#         super().__init__()
#         self.target = target
#         self.args = args
#
#     # 当调用函数的时候使用的方法
#     def run(self):
#
#         self.target(*self.args)
#
# def test(i):
#     time.sleep(i)
#     print('execute thread:{}'.format(i))
#
# def loop():
#     my_tasks = []
#     for i in range(5):
#         my_tasks.append(TestThread(target=test, args=(i,)))
#     for i in my_tasks:
#         i.start()
#     for i in my_tasks:
#         i.join()
#     print("all down")
# loop()


import threading
import time

a = 0
def add():
    global a
    for i in range(1000000):
        a += 1
def minus():
    global a
    for i  in range(1000000):
        a -= 1
def main():
    t1=threading.Thread(target=add)
    t2=threading.Thread(target=minus)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    time.sleep(2)
    print(a)
if __name__ == '__main__':
    main()
