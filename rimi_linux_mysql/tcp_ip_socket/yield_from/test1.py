def test1():
    print('start')
    while True:
        r = yield 'test1'
        print(r)
        if r == "1":
            return 'stop'


t = test1()
next(t)
t.send('4')
t.send('8')
t.send('1')
