#yield from


def count():
    print('新的count----')
    total = 0.0
    avg = 0.0
    num = 0
    while True:
        data = yield avg
        if not data:
            break
        total += data
        num += 1
        avg = total / num
        print(avg)
    print('完成count')
    return num, avg


def pipe(res, key):
    print('新的协程')
    while True:
        # try:
        yield from count()
        # print('统计{}数据完成'.format(key))

    # except StopIteration:
    #     print('已经不能运行')

    print('新的协程')


def start(data):
    res = {}
    for k, v in data.items():
        # print(k,v)
        group = pipe(res, k)
        next(group)
        for v1 in v:
            group.send(v1)
        group.send(None)
    # print(res)


data = {
    """
    成绩
    """
    'A班': [90, 89, 60, 68],
    'B班': [90, 13, 43, 13, 53],
    'C班': [12, 86, 43, 34, 89, 98, 89]
}

#1. yield from

def yield1(n):
    for i in range(n):
        yield i

def yield2(n):
    yield from range(n)
#yield1 yield2相互代替
#
# print(next(y))
# print(next(y))
# print(next(y))
#可以迭代可迭代对象
#一切皆对象
#字符串对象
#对象里面有很多方法
#__iter__或者 __next__() __getitem__()

x = "adsf"
num = 23232323
for i in x:
    print(i)
for i in yield2(100000):
    print(i)
#return

#yield from 第二个作用 建立一个管道,使用调用者能调用被调用者