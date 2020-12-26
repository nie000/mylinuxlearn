def avg_count():
    avg = 0
    count = 0
    total = 0
    while True:
        new_num = yield avg
        total += new_num
        try:
            avg = total/count
        except ZeroDivisionError:
            print(avg)

        except StopIteration:
            return 90

        finally:
            count +=1




a = avg_count()
print(next(a))
print(a.send(4))
print(a.send(9))
a.close()
try:
    print(a.send(7))
except Exception as e:
    print(e.value)
print(a.send(6))
