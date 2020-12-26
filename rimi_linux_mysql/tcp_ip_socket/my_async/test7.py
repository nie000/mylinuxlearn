import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
def call_back(x):
    time.sleep(3)
    print('get',x)

def stoploop(loop):
    loop.stop()
    time.sleep(4)
    loop.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    ex = ThreadPoolExecutor(max_workers=10)
    tasks = list()
    for i in range(20):
        tasks.append(loop.run_in_executor(ex,call_back,3))

    loop.run_until_complete(asyncio.wait(tasks))