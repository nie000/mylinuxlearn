import random
def test1():
    total = 0
    while True:
        x = yield
        if x is None:
            return total
        total += x

def test2(lists):
    while 1:
        res = yield from test1()
        lists.append(res)

if __name__ == '__main__':
    lists = []
    tmp = test2(lists)
    next(tmp)
    for i in range(5):
        for j in range(random.randint(4,8)):
            tmp.send(random.randint(4,9))
        tmp.send(None)

    print(lists)
