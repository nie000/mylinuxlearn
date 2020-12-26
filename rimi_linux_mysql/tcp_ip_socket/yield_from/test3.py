import time
from inspect import getgeneratorstate

def f():
    avg = 0
    total = 0
    count = 0
    while True:
        print('f is control')
        # print(avg)
        try:
            res = yield avg
            if res is None:
                print('f 自己关闭')
                # 在协程里面使用return 1.可以返回值,2.抛错
                return total, avg, count
            count += 1
            total += res
            avg = total / count
        except Exception:
            print('收到')

# 控制权
def main():
    x = f()
    print(getgeneratorstate(x))
    next(x)
    print(getgeneratorstate(x))
    print('main is control')

    res = f1(9.7)

    x.send(9.7)
    x.send(5.8)
    x.send(3)
    x.send(6)
    x.send(1)
    x.send(1)
    try:
        x.send(None)
    except StopIteration as e:
        print(e.value)
    print(getgeneratorstate(x))
    # x.close()
    x.throw(Exception)
    # throw 主控制函数向协程抛错误
    # #协程可以向控制方抛出异常，让控制方报错
    # print(getgeneratorstate(x))
    # try:
    #     next(x)
    #     x.send(1)
    # except StopIteration:
    #     print('stopped')
    # x.send(1)
    # print(getgeneratorstate(x))


# next send close 关闭协程
main()
