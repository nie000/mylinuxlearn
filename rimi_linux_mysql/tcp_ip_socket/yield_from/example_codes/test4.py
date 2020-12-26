class DemoException(Exception):
    pass

def test1():
    print('start')

    while True:
        try:
            x = yield
        except DemoException:
            print('demo ex')
        except StopIteration:
            print('asdf')
        else:
            print('receive:',x)

t = test1()

next(t)
t.send(6)
t.throw(DemoException)
t.send(9)
t.throw(StopIteration)
t.send(20)