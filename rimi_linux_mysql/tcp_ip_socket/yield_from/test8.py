# yield from
import random

a1 = 'abcdefg'

def f1():
    for i in a1:
        x = yield i
        if x == 3:
            return 3

# 新的语法结构
# 1. yield from 遍历并且生成值
# 2. yield from 可以作为协程的连接器
def f2():
    x = yield from f1()
    print('收到的值', x)
    return 8

# 控制权
def main():
    x = f2()
    next(x)
    while True:
        try:
            x.send(random.randint(0, 4))
        except StopIteration as e:
            print('mian 收到的值', e.value)
            break
main()
