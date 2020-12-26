from tornado.httpclient import AsyncHTTPClient
import asyncio
import time
num = 1
now = time.time()
async def f(url):
    global num
    num += 1

    # print(num)
    # print(time.time()-now)
    http_client = AsyncHTTPClient()
    try:
        response = await http_client.fetch(url)
        print(response.body)
    except Exception as e:
        print("Error: %s" % e)
        pass
    else:
        print(response.body)
        pass

#事件驱动

url = "http://gmtly.xianxia.yileweb.com/api/37wan/login?user_name=wx_i3519527&server_id=91&time=1543975963&is_adult=0&client=1&pt_vip=0&lingpai=0&user_info_filled=0"

#
# url = "http://blog.jobbole.com/{}/"
tasks = list()
for i in range(0,5000):
    tasks.append(f(url.format(url)))

print('--------')
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
print('--------')

secs = time.time() - now
print(secs)
