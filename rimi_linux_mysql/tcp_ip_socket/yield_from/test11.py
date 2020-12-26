def f1():
    print('1')

def f2():
    print('1')
    yield 2
# python 编译器
x1 = f1()
print('x1',x1)
x2 = f2()
print('x2',x2)