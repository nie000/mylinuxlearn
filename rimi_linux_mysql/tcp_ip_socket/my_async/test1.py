import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
def call_back1(x):
    print('call_back1 start')
    time.sleep(2)
    print('call_back over')

def call_back(x):
    print('call_back start')
    time.sleep(3)
    print('call_back over')
async def f1():
    print('f1 start')
    await asyncio.sleep(1)
    print('f1 over')
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    ex = ThreadPoolExecutor(max_workers=5)
    tasks = list()
    tasks1 = list()
    tasks2 = list()
    for i in range(10):
        tasks2.append(loop.run_in_executor(ex,call_back1,3))
    for i in range(10):
        tasks.append(loop.run_in_executor(ex,call_back,3))
    for i in range(10):
        tasks1.append(f1())
    loop.run_until_complete(asyncio.gather(*tasks1,*tasks,*tasks2))