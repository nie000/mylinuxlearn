from inspect import getgeneratorstate
def simple_gen1():
    print('started')
    x = yield 'running'
    print('receive_x:',x)
    y = yield x
    print('receive_y:', y)


test1 = simple_gen1()

print(getgeneratorstate(test1))

next(test1)
print(getgeneratorstate(test1))
next(test1)
print(getgeneratorstate(test1))
# try:
next(test1)
# except Exception:
#     pass
# print(getgeneratorstate(test1))
#
# next(test1)