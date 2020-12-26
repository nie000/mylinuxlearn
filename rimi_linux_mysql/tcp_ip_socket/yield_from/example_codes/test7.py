def test():
    for i in 'ab':
        yield i

    for i in range(5):
        yield i

print(list(test()))
def test1():
    yield from 'ab'
    yield from range(5)
print(list(test1()))