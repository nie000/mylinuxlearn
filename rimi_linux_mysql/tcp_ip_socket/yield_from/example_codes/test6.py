import time
import random

def consume():
    while True:
        product = yield
        print('consume product:',product)
        if product == 5:
            return '收到5'

def product():
    t = consume()
    while True:
        time.sleep(random.randint(0,1))
        t.send(random.randint(1,10))


product()
