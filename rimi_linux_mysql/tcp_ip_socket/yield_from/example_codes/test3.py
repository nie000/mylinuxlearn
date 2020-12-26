def sum():
    avg = None
    total = 0.0
    num = 0

    while True:
        r = yield avg
        total += r
        num += 1
        avg = total/num



test = sum()
next(test)
print(test.send(1))
print(test.send(5))
print(test.send(9))
print(test.send(89))