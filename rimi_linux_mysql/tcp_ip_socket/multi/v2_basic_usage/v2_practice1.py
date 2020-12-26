#封装http请求报文 多线程请求和单线程请求的不同
from http_req import get_url
from urllib.parse import urljoin
from v2_class_usage import TestThread
import time


def loop1():
    #单线程获取方式
    # http://blog.jobbole.com/114297/
    domain = "http://blog.jobbole.com/"
    for i in range(114297,114320):
        i = str(i)
        url = urljoin(domain,i)
        t = TestThread(target=get_url,args=(url,))
        t.start()



if __name__ == "__main__":
    t1 = time.time()
    loop1()

    t2 = time.time()

    print('---------')
    print(t2-t1)