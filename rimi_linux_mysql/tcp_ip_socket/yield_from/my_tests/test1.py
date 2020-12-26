def test1():
    while True:
        x = yield
        print(x)

def test2():
    yield from test1()

if __name__ == '__main__':
    test = test2()
    next(test)
    test.send(4)
    test.send(4)
    test.send(8)
    test.throw(StopIteration)