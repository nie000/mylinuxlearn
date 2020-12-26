def f1():
    l1 = []
    l2 = []
    print('function start')
    while 1:
        try:
            rec = yield
            print(rec)
            if isinstance(rec, int):
                l1.append(rec)
            if isinstance(rec, str):
                l2.append(rec)
        except Exception:
            return l1,l2


f =f1()

next(f)
f.send(1)
f.send(2)
f.send('saf')
f.send('13')

try:
    f.throw(StopIteration)
except Exception as e:
    x = e.value

print(x)