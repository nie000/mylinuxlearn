def reader():
    for i in range(4):
        yield "<<{}".format(i)


# def reader_wrapper(g):
#     for i in g:
#         yield i

def reader_wrapper(g):
    yield from g


wrap = reader_wrapper(reader())

for i in wrap:
    print(i)
