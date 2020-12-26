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
            print('当前没有值')
        except Ex:
            print('停止错误')
            return 5
class Ex(Exception):
    pass
counter = avg()
counter.send(None)
# send 错误
while True:
    num = input('请输入数字:')
    try:
        num = float(num)
    except Exception:
        try:
            counter.throw(Ex)
        except StopIteration as e:
            print('生成器已经停止')
            print(e.value)
        continue
    counter.send(num)

# return 他可以向我们这边抛出stopiteration
# return 他可以像我们返回值
# return 关闭我们的生成器
# 协程返回值是放在 stopiteration

# 1. 定义的时候加上 yield  变成生成器
# 2. yield 可以暂停我们代码
# 3. yield 右边是去抛出值
# 4. yield 左边是去接收生成器对象 send过来的值
# 5. next send(None) 激活生成器
# 6. 生成器停止的时候会抛出 stopiteration的错误 (向调用方抛出)
# 7. throw(ex) 是可以向生成器中抛出异常
# 8. 生成器中使用return关键字,会关闭生成器,并且向调用方抛出stop异常,然后把值放在异常的value里面
