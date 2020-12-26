# 生产者 消费者模式

# 工厂 会不会关心你要买了才生产?
# 顾客 你也不会关心工厂有还剩多少瓶水
import time
import random
import threading

product_list = []
num = 0

def product_num():
    global num
    while 1:
        num += 1
        product_time = random.randint(1,3)
        time.sleep(product_time)
        print('product num:',num)
        product_list.append(num)


def get_num():
    """
    获取商品
    :return:
    """
    while 1:
        try:
            num = product_list.pop()
            consume_num(num)
        except Exception:
            continue


def consume_num(num):
    consum_time = random.randint(1, 3)
    time.sleep(consum_time)
    print('consume product',num)


def start():
    t1 = threading.Thread(target=product_num)
    t1.start()
    time.sleep(5)
    t2 = threading.Thread(target=get_num)
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    start()
