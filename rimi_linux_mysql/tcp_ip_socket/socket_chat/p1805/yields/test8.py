# yield from

# def for_test():
#     # for i in 'ab':
#     #     yield i
#     #等价的
#     yield from 'ab'


# t = for_test()

# for i in t:
#     print(i)

# yield from
# def test1():
#     yield from 'ab'
#     yield from range(5)

# t = test1()
#
# for i in t:
#     print(i)

#1 .如果yield from 只是替代for i in t： yield ipython是不会纳入

#2. 作为协程调用者和被调用者之间的通道


# 无限的计算平均值

# 输入:   1.  5-->5   2.  3 --->8    3. 2--->10  4. 2---->12
# 输出:   1.  5       2.  4          3. 3.333    4. 3
def avg():
    num = 0
    total = 0.0
    # 无限的循环
    while 1:
        # 接收一个值
        try:
            val = yield
            # 计算次数+1
            num += 1
            total += val
            # 平均数等于总数/计算次数
            avg = total / num
            print('当前平均数{}'.format(avg))
        except IndexError:
            return 1
        except Ex:
            print('停止错误')
            return 5
class Ex(Exception):
    pass


# send 错误
# #在loop 和 avg之间加一个通道

def pipe1():
    yield from avg()


def pipe():
    # counter = avg()
    # next(counter)
    # while True:
    #     num = yield
    #     try:
    #         counter.send(num)
    #     except IndexError:
    #         try:
    #             counter.throw(IndexError)
    #         except StopIteration as e:
    #             num = e.value
    #             return num
    #         return num
    #     except StopIteration:
    #         return num
    #     except IndentationError:
    #         return num
    num = yield from pipe1()
    print('在pip中{}'.format(num))

def loop2():
    p = pipe()
    next(p)
    while True:
        num = input('请输入数字:')
        try:
            num = float(num)
        except StopIteration as e:
            print(e.value)
            continue
        p.send(num)

def loop1():
    p = pipe()
    next(p)
    while True:
        num = input('请输入数字:')
        try:
            num = float(num)
        except StopIteration as e:
            print(e.value)
            continue
        p.send(num)

def loop():
    p = pipe()
    next(p)
    while True:
        num = input('请输入数字:')
        try:
            num = float(num)
        except Exception:
            try:
                p.throw(Ex)
            except StopIteration as e:
                print('生成器已经停止')
                print(e.value)
            continue
        p.send(num)

#yield from

loop()