# import threading
# from dis import dis
#
# a = 0
# lock = threading.Lock()
# def add():
#     global a
#     for i in range(1000000):
#         lock.acquire()  #获得锁,互斥锁
#         lock.acquire()
#         a += 1
#         lock.release()   #释放锁
#         lock.release()
# def minus():
#     global a
#     for i in range(1000000):
#         lock.acquire()
#         a -= 1
#         lock.release()
# if __name__ == '__main__':
#     t1 = threading.Thread(target=add)
#     t2 = threading.Thread(target=minus)
#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()
#     print(a)


# import threading
# from dis import dis
#
# a = 0
# lock = threading.RLock()  # 重载锁
# def add():
#     global a
#     lock.acquire()  # 获得锁
#     print('111111')
#     for i in range(1000000):
#         lock.acquire()  # 释放锁
#         a += 1
#         lock.release()   #释放锁
#     print('2222222')
#     lock.release()
# def minus():
#     global a
#     print('33333333')
#     for i in range(1000000):
#         lock.acquire()
#         a -= 1
#         lock.release()
#     print('44444444')
# if __name__ == '__main__':
#     t1 = threading.Thread(target=add)
#     t2 = threading.Thread(target=minus)
#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()
#     print(a)