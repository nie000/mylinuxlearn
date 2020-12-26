def sum():
    avg = None
    total = 0.0
    num = 0

    while True:
        r = yield avg
        if r is None:
            break
        total += r
        num += 1
        avg = total/num

    return num,avg

s1 = sum()

next(s1)
s1.send(5)
s1.send(8)
s1.send(10)

try:
    s1.send(None)
except Exception as e:
    print(e.value)