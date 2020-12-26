def coro(a):
    print('res:',str(a))
    b = yield a
    print('res', str(a+b))
    c = yield b
    print('res', str(a + c))
    


test1 = coro(5)
#什么都不会打印
next(test1)
# res 5
t1 = test1.send(6)
# 11
t2 = test1.send(9)

# 14


