import asyncio
import requests
import time


# 异步库,里面的所有程序都不会阻塞
# 装饰器 强制加上装饰器 使他变成协程
# 异步库里面的代码都必须是非阻塞的
# yield from 有两个作用 python3.5之后
def get1():
    # time.sleep(6)
    yield from asyncio.sleep(6)
    print('async 1')
    for i in range(10000):
        print(515)

def get2():
    requests.get('55454545')
    yield
    print('async 2')
# async await代替 yield from
async def get3():
    await asyncio.sleep(5)
    print('async 3')
def loop():
    # 固定用法 while True:
    tasks = [get1(), get2()]
    loop = asyncio.get_event_loop()
    # 由我们的loop自己去排定什么时候去调用
    loop.run_until_complete(asyncio.wait(tasks))


loop()
