def reader():
    while 1:
        x =yield
        print('recv',x)


# def reader_wrapper():
#     r = reader()
#     next(r)
#     while 1:
#         try:
#             x = yield
#             r.send(x)
#         except Exception:
#             print('break')
#             break



def reader_wrapper():
    yield from reader()

j = reader_wrapper()

next(j)
j.send(3)
j.send(3)
j.send(3)
j.throw(StopIteration)
