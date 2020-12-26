from inspect import getgeneratorstate


def coro(a):
    print('res:', str(a))
    b = yield a
    print('res', str(a + b))
    c = yield b
    print('res', str(b + c))


test1 = coro(5)
print(getgeneratorstate(test1))
res1 = next(test1)
print(getgeneratorstate(test1))
res2 = test1.send(6)
print(getgeneratorstate(test1))
try:
    test1.send(9)
except StopIteration:
    print('结束了')
print(getgeneratorstate(test1))
