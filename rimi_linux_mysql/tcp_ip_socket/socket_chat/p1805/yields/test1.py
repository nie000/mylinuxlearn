# 生成 计数
#生成器对象 加了yield之后,就会变成生成器对象
def simple_gen1():
    print('started')
    x = yield 'running'
    print(x)
    print('ending')


def simple_gen2():
    print('started')
    print('asdfasd')
    return 'running'


#初始化生成器对象
test1 = simple_gen1()
# test2 = simple_gen2()

# print(test2)

# python 动态语言
# 代码 --->    python解释器  |||||||||-----> 中间代码----> 链接 --->源代码
#列表生成式
#预激生成器 激活
#预激的时候,必须使用send(None) 或者使用 next()
t1 = test1.send(None)
t2 = test1.send('hello')
# print(t1)
print(t2)
# next(test1)


#激活后 代码会向下运行,直到遇到 yield 停止(yield可以暂停代码)
# 1. yield 暂停
# 2. yield 生成
# 3. yield 接收值  使用send代替next send 1. next激活生成器 2.向生成器中发送值,发送到yield左边