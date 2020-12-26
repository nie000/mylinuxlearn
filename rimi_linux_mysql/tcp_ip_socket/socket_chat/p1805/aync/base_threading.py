#asyncio的基本使用方式

import time
import threading

def get1():

    time.sleep(2)

    print('成功')

def get2():
    time.sleep(3)
    print('成功')
    #多线程用法
threading.Thread(target=get1).start()
threading.Thread(target=get2).start()

