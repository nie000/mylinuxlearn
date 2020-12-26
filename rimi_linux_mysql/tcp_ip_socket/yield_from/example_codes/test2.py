def coro(a):
    print('res:',str(a))
    b = yield a
    print('res', str(a+b))
    c = yield b
    print('res', str(a + c))

test1 = coro(5)

next(test1)
test1.send(6)
test1.send(9)