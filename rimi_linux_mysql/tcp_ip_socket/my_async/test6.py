import asyncio
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
    now = loop.time()
    loop.call_at(now+3,call_back,32)
    loop.call_at(now+2, call_back, 31)
    loop.call_soon_threadsafe()
    loop.run_forever()